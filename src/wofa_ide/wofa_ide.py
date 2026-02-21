# WOFA_IDE.py
import sys
import os
import tkinter

from py_libraries.LanguageOp import *

from editors import *
from app_info import *

import requests

PROJECT_FILE_EXT = "wfa"
IS_DEBUG=False
IS_CHECK_ACTIVATION=False
IS_LOG=False


def setup_logging():
    log_filename = f"wofa_ide_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("=" * 50)
    logging.info("WOFA IDE Application Started")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current directory: {os.getcwd()}")
    logging.info(f"Files in directory: {os.listdir('.')}")


def excepthook(exc_type, exc_value, exc_traceback):
    """全局异常处理"""
    error_msg = f"未捕获的异常: {exc_type.__name__}: {exc_value}"
    logging.error(error_msg, exc_info=(exc_type, exc_value, exc_traceback))

    # 显示错误信息给用户
    traceback_details = "\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_display = f"程序发生严重错误:\n\n{str(exc_value)}\n\n详细信息已保存到日志文件"
    #show_error_dialog("程序错误", error_display)

    sys.exit(1)


# ================= 初始化 =================
if IS_LOG:
    setup_logging()
    sys.excepthook = excepthook

# 资源路径处理函数
def get_full_path(relative_path):
    """获取资源的绝对路径"""
    try:
       # if hasattr(sys, '_MEIPASS'):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            # 取得當前執行腳本 (.py) 的絕對路徑，並向上推導至正確位置
            # __file__ 是當前檔案的完整路徑
            base_path = os.path.dirname(os.path.abspath(__file__))
            #base_path = os.path.abspath(".")
            #base_path = os.path.dirname(__file__).parent

        full_path = os.path.join(base_path, relative_path)

        if not os.path.exists(full_path):
            if IS_LOG:
                logging.error(f"资源文件未找到: {full_path}")
            #show_error_dialog("文件缺失", f"找不到必需的文件: {relative_path}")
            sys.exit(1)

        return full_path
    except Exception as e:
        if IS_LOG:
            logging.error(f"资源路径错误: {str(e)}")
        #show_error_dialog("初始化错误", f"无法定位资源文件: {str(e)}")
        sys.exit(1)


# 加载资源文件
try:
    excel_path = get_full_path("languages.xlsx")
    logging.info(f"资源文件找到: {excel_path}")
except Exception as e:
    if IS_LOG:
        logging.error(f"资源文件加载失败: {str(e)}")
    #show_error_dialog("文件错误", f"无法加载资源文件: {str(e)}")
    sys.exit(1)

def check_activation():
        """检查是否已经激活"""
        # 这里可以添加更复杂的验证逻辑，如检查注册表或文件
        return os.path.exists("settings.json")

class Activation:
    def __init__(self, parent: TK_WINDOW, callback:callable):
        self.root = parent
        self.is_activated = False
        self.callback=callback

        self.show_activation_dialog()
        #self.destroy()

    def destroy(self):
        destroy_TK_WINDOW(self.root)
        self.root = None


    def show_activation_dialog(self):
        """显示激活对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("产品激活")
        dialog.geometry("400x250")
        dialog.grab_set()  # 模态对话框

        # 感谢购买标签
        tk.Label(dialog, text="感谢购买", font=("Arial", 16)).pack(pady=10)

        # 序列号输入
        tk.Label(dialog, text="产品序列号:").pack(pady=(10, 0))
        serial_entry = tk.Entry(dialog, width=30)
        serial_entry.pack()

        # 公司名称输入
        tk.Label(dialog, text="用户公司名称:").pack(pady=(10, 0))
        company_entry = tk.Entry(dialog, width=30)
        company_entry.pack()

        # 激活按钮
        def on_button_clicked():
            serial = serial_entry.get().strip()
            company = company_entry.get().strip()

            if not serial or not company:
                messagebox.showerror("错误", "请输入序列号和公司名称")
                return

            if self.send_activation(serial, company):
                messagebox.showinfo("成功", "产品激活成功！")
                self.is_activated=True
            else:
                messagebox.showerror("错误", "激活失败，请检查网络或联系供应商")

            #self.destroy()
            self.callback(self.is_activated)

        tk.Button(dialog, text="激活产品", command=on_button_clicked, width=15).pack(pady=20)

    def send_activation(self, serial, company):
        """发送激活信息到服务器"""
        try:
            response = requests.post(
                "https://syntak.net/activation.php",
                data={
                    'serial_no': serial,
                    'user_company': company
                },
                timeout=10
            )
            return response.status_code == 200 and response.text.strip() == "SUCCESS"
        except Exception as e:
            print(f"激活错误: {e}")
            return False


class WorkflowIDE:
    def __init__(self):
        self.translator = LanguageTranslator(get_full_path("languages.xlsx"))

        self.settings=None
        self.my_language=None
        self.root = tk.Tk()
        self.notebook = None
        self.edit_tab_text = None
        self.current_tab_index = -1
        self.list_project_pages: List[PROJECT_PAGE] = []

        self.list_embed_model = list(get_args(EMBED_MODELS))

        ai_nodes = [ENUM_NODE.NODE_ASK_LLM,
                   ENUM_NODE.NODE_CATEGORIZED_BY_LLM,
                   ENUM_NODE.NODE_KNOWLEDGE_RETRIEVER,
                   # ENUM_NODE.NODE_ASK_LLM_WITH_KNOWLEDGE,
                   ]
        ai_nodes += [ ENUM_NODE.NODE_OCR, ENUM_NODE.NODE_VOICE_RECOGNIZE,
                   ENUM_NODE.NODE_GENERATE_IMAGE_FROM_TEXT,
                   ENUM_NODE.NODE_TRANSLATED_BY_LLM] if not IS_LITE else []

        self.enum_node_categories = {
            'Logic': [ENUM_NODE.NODE_BRANCH, ENUM_NODE.NODE_ITERATION, ENUM_NODE.NODE_PYTHON_CODE_EXECUTOR,
                      ENUM_NODE.NODE_END],
            'AI': ai_nodes,
            'IO': [ENUM_NODE.NODE_HTTP_REQUEST, ENUM_NODE.NODE_SFTP_UPLOAD, ENUM_NODE.NODE_SEND_MAIL, ENUM_NODE.NODE_RECEIVE_MAIl,
                   ENUM_NODE.NODE_CRAWL, ENUM_NODE.NODE_EXTRACT_TEXT]
        }

        self.project_name_manager = NAME_MANAGER()
        self.frame_node_palette = None
        self.frame_notebook = None
        self.frame_node_configer = None
        self.float_btn_frame = None
        self.node_configer = None

        self.menubar: Optional[tk.Menu] = None
        self.file_menu: Optional[tk.Menu] = None
        self.insert_menu: Optional[tk.Menu] = None
        self.edit_menu: Optional[tk.Menu] = None
        self.debug_menu: Optional[tk.Menu] = None
        self.settings_menu: Optional[tk.Menu] = None
        self.new_button: Optional[tk.Button] = None
        self.open_button: Optional[tk.Button] = None
        self.save_button: Optional[tk.Button] = None
        self.save_all_button: Optional[tk.Button] = None
        self.save_as_button: Optional[tk.Button] = None
        self.print_button: Optional[tk.Button] = None
        self.close_button: Optional[tk.Button] = None
        self.run_button: Optional[tk.Button] = None
        self.step_run_button: Optional[tk.Button] = None
        self.single_node_run_button: Optional[tk.Button] = None
        self.stop_run_button: Optional[tk.Button] = None
        self.list_palette_button: Optional[List[tk.Button]] = []

       # self.configer_schedule: Optional[Configer_SCHEDULE_TIME] = None
        self.editor_settings_knowledge_collections: Optional[Editor_KNOWLEDGE_COLLECTIONS] = None
        #self.editor_knowledge_collections: Optional[Editor_KNOWLEDGE_COLLECTIONS] = None
        self.picker_knowledge_collections: Optional[Picker_KNOWLEDGE_COLLECTIONS] = None
        self.editor_settings_llms_api: Optional[Editor_LLMS_API] = None
        self.editor_llms_api: Optional[Editor_LLMS_API] = None
        self.editor_variables: Optional[Editor_VARIABLES] = None
        self.viewer_variables: Optional[Viewer_VARIABLES] = None

        self.tooltip = None
        self.tooltip_label = None
        #self.editor_server_url: Optional[Editor_LINE] = None
     #   self.editor_mount_manager: Optional[Editor_MOUNT_MANAGER] = None

        #if not IS_DEBUG:
        #    self.is_activated = self.check_activation()
        #    if not self.is_activated:
        #       self.show_activation_dialog()
        #    if not self.is_activated:
        #        return

        self.node_graphic_tmp = None

        if not IS_DEBUG and IS_CHECK_ACTIVATION:
            if not check_activation():
                self.activation = Activation(self.root, self.on_activation_checked)
        else:
            self.init()

    def init(self):
        self.settings = Settings()
        self.my_language = self.settings.get("language")
        #sys_lang = LanguageOp.get_current_input_language()
        if not self.my_language:
            sys_lang = get_current_input_language().get("language_name")
            if sys_lang in self.translator.get_languages():
               self.my_language = sys_lang
            else:
               self.my_language = self.translator.get_languages()[0]

        self.settings.set("language", self.my_language)
        self.translator.set_current_language(self.my_language)


        self.root.title(self.get_translation("app_title") )
        if sys.platform == 'win32':
            # Windows: 使用 zoomed
            self.root.state('zoomed')
        else:
            self.root.attributes('-fullscreen', True)


        if getattr(sys, 'frozen', False):
            # 編譯後的路徑
            base_path = Path(sys._MEIPASS)
            icon_path = base_path / APP_ICON
        else:
            # 開發時的路徑
            base_path = Path(__file__).parent
            icon_path = base_path / "images" / APP_ICON

        try:
            self.root.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"Error loading icon: {e}")
        #self.root.iconbitmap("syntak_blue_128.ico")

        #self.root.attributes('-fullscreen', True)
        # 获取屏幕分辨率
        #screen_width = int(self.root.winfo_screenwidth()*.75)
        #screen_height = int( self.root.winfo_screenheight()*.85)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 设置窗口大小与屏幕一致，并定位到左上角
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        setup_ttk_style()


        self.setup_menu()
        self.setup_toolbar()
        self.setup_main_ui()

    def on_activation_checked(self, is_activated:bool):
        if is_activated:
            self.init()
        else:
           if self.root:
              destroy_TK_WINDOW(self.root)
           sys.exit(2)

    def get_translation(self, key):
        return self.translator.get_translation(key, self.my_language)

    def set_language(self, language: str):
        self.my_language = language
        self.settings.set("language", self.my_language)
        self.translator.set_current_language(language)
        self.root.title(self.get_translation("app_title"))
        self.update_menus_language()
        self.update_choose_language_menu()
        self.node_configer.refresh()

    def update_menus_language(self):
        self.menubar.entryconfigure(1, label=self.get_translation("file"))
        self.menubar.entryconfigure(2, label=self.get_translation("insert"))
        self.menubar.entryconfigure(3, label=self.get_translation("edit"))
        self.menubar.entryconfigure(4, label=self.get_translation("debug"))
        self.menubar.entryconfigure(5, label=self.get_translation("settings"))


        self.file_menu.entryconfigure(0, label=self.get_translation("new"))
        self.file_menu.entryconfigure(1, label=self.get_translation("open"))
        self.file_menu.entryconfigure(2, label=self.get_translation("save"))
        self.file_menu.entryconfigure(3, label=self.get_translation("save_all"))
        self.file_menu.entryconfigure(4, label=self.get_translation("save_as"))
        self.file_menu.entryconfigure(5, label=self.get_translation("print"))
        self.file_menu.entryconfigure(7, label=self.get_translation("close"))
        # 直接修改按钮文本
        self.new_button.configure(text=self.get_translation("new"))
        self.open_button.configure(text=self.get_translation("open"))
        self.save_button.configure(text=self.get_translation("save"))
        self.save_all_button.configure(text=self.get_translation("save_all"))
        self.save_as_button.configure(text=self.get_translation("save_as"))
        self.print_button.configure(text=self.get_translation("print"))
        self.close_button.configure(text=self.get_translation("close"))

        j=0
        k=0
        for i, (category, enum_nodes) in enumerate(self.enum_node_categories.items()):

            for enum_node in enum_nodes:
                self.insert_menu.entryconfigure(j, label=self.get_translation(enum_node.value))
                self.list_palette_button[k].configure(text=self.get_translation(enum_node.value))
                j+=1
                k+=1

            is_last = i == len(self.enum_node_categories) - 1

            if not is_last:
                j+=1

        self.edit_menu.entryconfigure(0, label=self.get_translation("cut"))
        self.edit_menu.entryconfigure(1,label=self.get_translation("copy") )
        self.edit_menu.entryconfigure(2,label=self.get_translation("paste"))
        self.edit_menu.entryconfigure(4, label=self.get_translation("variables"))
        self.edit_menu.entryconfigure(5, label=self.get_translation("llms_api"))
        self.edit_menu.entryconfigure(6, label=self.get_translation("knowledge_collections"))
        # self.edit_menu.entryconfigure(3,label=self.get_translation("schedule"))
        #  self.edit_menu.entryconfigure(4, label=self.get_translation("mount_manager"))

        self.debug_menu.entryconfigure(0, label=self.get_translation("run"))
        self.debug_menu.entryconfigure(1,label=self.get_translation("step_run"))
        self.debug_menu.entryconfigure(2,label=self.get_translation("single_node_run"))
        self.debug_menu.entryconfigure(3,label=self.get_translation("stop_run"))
        self.run_button.configure(text=self.get_translation("run"))
        self.step_run_button.configure(text=self.get_translation("step_run"))
        self.single_node_run_button.configure(text=self.get_translation("single_node_run"))
        self.stop_run_button.configure(text=self.get_translation("stop_run"))

        self.settings_menu.entryconfigure(0, label=self.get_translation("language"))
        self.settings_menu.entryconfigure(1, label=self.get_translation("llms_api"))
        self.settings_menu.entryconfigure(2, label=self.get_translation("knowledge_collections"))


    def update_choose_language_menu(self):
        for i in range(0, self.choose_language.index("end") + 1):
            try:
                label = self.choose_language.entrycget(i, "label")
                if label == self.my_language:
                    # 高亮當前選擇的語言
                    self.choose_language.entryconfigure(
                        i,
                        background="#4a6baf",  # 藍色背景
                        foreground="white",  # 白色文字
                        activebackground="#4a6baf",
                        activeforeground="white"
                    )
                else:
                    # 重置其他語言的顏色（恢復默認）
                    self.choose_language.entryconfigure(
                        i,
                        background="SystemButtonFace",  # 系統默認背景色
                        foreground="SystemWindowText",  # 系統默認文字色
                        activebackground="SystemHighlight",  # 系統默認懸停背景
                        activeforeground="SystemHighlightText"  # 系統默認懸停文字
                    )
            except tk.TclError:
                continue
    def setup_menu(self):
        # 菜单栏实现
        self.menubar = tk.Menu(self.root)
        
        # File菜单
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label=self.get_translation("new"), command=self.new_project)
        self.file_menu.add_command(label=self.get_translation("open"), command=self.open_project)
        self.file_menu.add_command(label=self.get_translation("save"), command=self.save_project, state="disabled")
        self.file_menu.add_command(label=self.get_translation("save_all"), command=self.save_all_projects, state="disabled")
        self.file_menu.add_command(label=self.get_translation("save_as"), command=self.save_project_as, state="disabled")
        self.file_menu.add_command(label=self.get_translation("print"), command=self.print_project,
                                   state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.get_translation("close"), command=self.close_project, state="disabled")
        self.menubar.add_cascade(label=self.get_translation("file"), menu=self.file_menu)
        
        # Nodes菜单
        self.insert_menu = tk.Menu(self.menubar, tearoff=0)

        for i, (category, enum_nodes) in enumerate(self.enum_node_categories.items()):

            for enum_node in enum_nodes:
                self.insert_menu.add_command(
                    label=title(self.get_translation(enum_node.value)),
                    command=lambda nt=enum_node: self.handle_insert_menu_clicked(nt),
                    state=tk.DISABLED
                )

            is_last = i == len(self.enum_node_categories) - 1

            if not is_last:
                self.insert_menu.add_separator()

        self.menubar.add_cascade(label=self.get_translation("insert"), menu=self.insert_menu)

        # Edit菜单
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label=self.get_translation("cut"), command=self.edit_cut,
                                   state="disabled")
        self.edit_menu.add_command(label=self.get_translation("copy"), command=self.edit_copy,
                                   state="disabled")
        self.edit_menu.add_command(label=self.get_translation("paste"), command=self.edit_paste,
                                   state="disabled")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self.get_translation("variables"), command=self.edit_variables,
                                   state="disabled")
        self.edit_menu.add_command(label=self.get_translation("llms_api"), command=self.edit_llms_api, state="disabled")
        self.edit_menu.add_command(label=self.get_translation("knowledge_collections"),
                                   command=self.pick_knowledge_collections, state="disabled")
        # self.edit_menu.add_command(label=self.get_translation("schedule"), command=self.edit_schedule, state="disabled")
        # self.edit_menu.add_command(label=self.get_translation("server_url"), command=self.edit_server_url, state="disabled")
       #self.edit_menu.add_command(label=self.get_translation("mount_manager"),
       #                           command=self.edit_mount_manager, state="disabled")
        #self.edit_menu.add_command(label=self.get_translation("knowledge_collections"),
        #                           command=self.edit_knowledge_collections, state="disabled")


        self.menubar.add_cascade(label=self.get_translation("edit"), menu=self.edit_menu)
        
        # Debug菜单
        self.debug_menu = tk.Menu(self.menubar, tearoff=0)
        self.debug_menu.add_command(label=self.get_translation("run"), command=self.run, state="disabled")
        self.debug_menu.add_command(label=self.get_translation("step_run"), command=self.step_run, state="disabled")
        self.debug_menu.add_command(label=self.get_translation("single_node_run"), command=self.single_node_run, state="disabled")
        self.debug_menu.add_command(label=self.get_translation("stop_run"), command=self.stop_run, state="disabled")
        self.menubar.add_cascade(label=self.get_translation("debug"), menu=self.debug_menu)

        # Settings菜单
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_translation("settings"), menu=self.settings_menu)

        self.choose_language = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.get_translation("language"), menu=self.choose_language)
        for language in self.translator.get_languages():
            self.choose_language.add_command(label=language, command=lambda lang=language: self.set_language(lang))
        self.update_choose_language_menu()

        self.settings_menu.add_command(label=self.get_translation("llms_api"), command=self.edit_settings_llms_api)
        self.settings_menu.add_command(label=self.get_translation("knowledge_collections"), command=self.edit_settings_knowledge_collections)


        self.root.config(menu=self.menubar)

    def enable_pallet_buttons(self, is_enabled: True):
        enabled = tk.NORMAL
        if not is_enabled:
            enabled = tk.DISABLED

        for i in range(0, len(self.list_palette_button)):
            try:
                self.list_palette_button[i].configure(state=enabled)
            except:
                pass  # 跳過分隔線等不可禁用的項目

    def enable_insert_menu(self, is_enabled: True):
        enabled = tk.NORMAL
        if not is_enabled:
            enabled = tk.DISABLED

        for i in range(0, self.insert_menu.index("end") + 1):
            try:
                self.insert_menu.entryconfigure(i, state=enabled)
            except:
                pass  # 跳過分隔線等不可禁用的項目

    def enable_edit_menu(self, is_enabled: bool = True, start: int=-1, end:int=-1):
        enabled = tk.NORMAL
        if not is_enabled:
            enabled = tk.DISABLED

        if start<0:
            start = 0
        if end < 0:
            end = self.edit_menu.index("end") + 1

        for i in range(start, end):
            try:
                self.edit_menu.entryconfigure(i, state=enabled)
            except:
                pass  # 跳過分隔線等不可

    def enable_debug_menu(self, is_enabled: True):
        enabled = tk.NORMAL
        if not is_enabled:
            enabled = tk.DISABLED

        for i in range(0, self.debug_menu.index("end") + 1):
            try:
                self.debug_menu.entryconfigure(i, state=enabled)
            except:
                pass  # 跳過分隔線等

        self.run_button.configure( state=enabled)
        self.step_run_button.configure( state=enabled)
        self.single_node_run_button.configure( state=enabled)
        self.stop_run_button.configure( state=enabled)

    def handle_insert_menu_clicked(self, enum_node: ENUM_NODE):
        self.list_project_pages[self.current_tab_index].enum_canvas_operation = ENUM_CANVAS_OPERATION.ADD_NODE
        self.list_project_pages[self.current_tab_index].enum_node_to_insert = enum_node

    def setup_toolbar(self):
        """创建工具栏（位于菜单栏下方）"""
        self.toolbar = ttk.Frame(self.root, padding=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.toolbar_general = ttk.Frame(self.toolbar)
        self.toolbar_general.pack(side=tk.LEFT, fill=tk.X)
        # 工具栏按钮（使用文本和简单样式）
        self.new_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("new"),
            command=self.new_project,
            style="Toolbutton"
        )
        self.new_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.open_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("open"),
            command=self.open_project,
            style="Toolbutton"
        )
        self.open_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("save"),
            command=self.save_project,
            state="disabled",
            style="Toolbutton"
        )
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_all_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("save_all"),
            command=self.save_all_projects,
            state="disabled",
            style="Toolbutton"
        )
        self.save_all_button .pack(side=tk.LEFT, padx=2, pady=2)

        self.save_as_button  = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("save_as"),
            command=self.save_project_as,
            state="disabled",
            style="Toolbutton"
        )
        self.save_as_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.print_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("print"),
            command=self.print_project,
            state="disabled",
            style="Toolbutton"
        )
        self.print_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.close_button = ttk.Button(
            self.toolbar_general,
            text=self.get_translation("close"),
            command=self.close_project,
            state="disabled",
            style="Toolbutton"
        )
        self.close_button.pack(side=tk.LEFT, padx=2, pady=2)


        self.toolbar_debug = ttk.Frame(self.toolbar)
        self.toolbar_debug.pack(side=tk.RIGHT, fill=tk.X)
        self.run_button = ttk.Button(
            self.toolbar_debug,
            text=self.get_translation("run"),
            command=self.run,
            state="disabled",
            style="Toolbutton"
        )
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.step_run_button = ttk.Button(
            self.toolbar_debug,
            text=self.get_translation("step_run"),
            command=self.step_run,
            state="disabled",
            style="Toolbutton"
        )
        self.step_run_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.single_node_run_button = ttk.Button(
            self.toolbar_debug,
            text=self.get_translation("single_node_run"),
            command=self.single_node_run,
            state="disabled",
            style="Toolbutton"
        )
        self.single_node_run_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.stop_run_button = ttk.Button(
            self.toolbar_debug,
            text=self.get_translation("stop_run"),
            command=self.stop_run,
            state="disabled",
            style="Toolbutton"
        )
        self.stop_run_button.pack(side=tk.LEFT, padx=2, pady=2)

    def setup_main_ui(self):
        # 三栏主界面布局
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧节点面板
        self.frame_node_palette = ttk.Frame(main_frame, width=200)
        self.frame_node_palette.pack(side=tk.LEFT, fill=tk.Y)
        #self.frame_node_palette.grid(row=0, column=0, sticky="wns")
        
        # 中间画布区域

        self.frame_notebook = ttk.Frame(main_frame)
        self.frame_notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #self.frame_notebook.grid(row=0, column=1, sticky="nsew")
        self.notebook = ttk.Notebook(self.frame_notebook)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        #self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.bind("<Double-Button-1>", self.on_notebook_clicked)
        self.notebook.bind("<Enter>", self.on_notebook_enter)
        self.notebook.bind("<Leave>", self.on_notebook_leave)
        self.notebook.bind("<Motion>", self.on_notebook_motion)

        # 右侧配置面板
        self.frame_node_configer = ttk.Frame(main_frame, width=300)
        self.frame_node_configer.pack(side=tk.RIGHT, fill=tk.Y)
        #self.frame_config_node.grid(row=0, column=2, sticky="nse")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        llms_api = None
        if self.current_tab_index>=0:
            llms_api = self.list_project_pages[self.current_tab_index].project.llms_api

        self.node_configer = Node_Configer(self.frame_node_configer, callback_node_changed=self.on_node_changed, callback_name_changed=self.on_name_changed,
                                         #  llms_api=self.settings.llms_api,
                                         #  llms_api=llms_api,
                                           list_embed_model_name= self.list_embed_model,
                                          # settings_knowledge_collections=self.settings.knowledge_collections,
                                           translator=self.translator)
        # 画布交互初始化

        # 初始化节点面板
        self.init_node_palette()
        #self.init_floating_zoom_buttons(self.frame_notebook)
        self.init_floating_zoom_slider(self.frame_notebook)

    def on_notebook_enter(self, event):
        """滑鼠進入 notebook"""
        pass

    def on_notebook_leave(self, event):
        """滑鼠離開 notebook"""
        self.hide_tooltip()

    def on_notebook_motion(self, event):
        """滑鼠在 notebook 上移動"""
        # 檢查是否在 tab 標籤區域
        tab_id = self.notebook.identify(event.x, event.y)
        if "label" in tab_id:
            index = self.notebook.index(f"@{event.x},{event.y}")
            if 0 <= index < len(self.list_project_pages):
                project_page = self.list_project_pages[index]
                file_path = project_page.project.project_file_path

                if file_path and os.path.exists(file_path):
                    # 顯示完整檔案路徑
                    self.show_tooltip(event.x_root, event.y_root, file_path)
                else:
                    # 新專案，顯示未保存
                    self.show_tooltip(event.x_root, event.y_root, self.get_translation("unsaved_project"))
            else:
                self.hide_tooltip()
        else:
            self.hide_tooltip()

    def show_tooltip(self, x, y, text):
        """顯示工具提示"""
        if self.tooltip is None:
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x + 10}+{y + 10}")

            self.tooltip_label = ttk.Label(
                self.tooltip,
                text=text,
                background="#ffffcc",
                relief="solid",
                borderwidth=1,
                padding=(5, 2),
                font=("Arial", 9)
            )
            self.tooltip_label.pack()

            # 確保提示框在頂層
            self.tooltip.attributes('-topmost', True)
        else:
            self.tooltip_label.config(text=text)
            self.tooltip.wm_geometry(f"+{x + 10}+{y + 10}")

    def hide_tooltip(self):
        """隱藏工具提示"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            self.tooltip_label = None

    def init_floating_zoom_slider(self, parent):
        """创建悬浮缩放控制面板（使用滑动条）"""
        # 创建透明容器
        self.float_zoom_frame = ttk.Frame(parent)
        self.float_zoom_frame.place_forget()

        # 配置滑动条样式
        style = ttk.Style()
        #style.configure("Zoom.Horizontal.TScale",
        style.configure("Zoom.Vertical.TScale",
                        troughcolor='#E0E0E0',
                        sliderlength=20,
                        sliderthickness=10)
        style.configure("Zoom.TFrame", background='#FFFFFF')

        # 创建滑动条
        self.zoom_slider = ttk.Scale(
            self.float_zoom_frame,
            from_=1.0,  # 最小缩放比例
            to=0.1,  # 最大缩放比例
            value=1.0,  # 初始值
            orient=tk.VERTICAL,
            length=120,
            command=self._on_zoom_slide,
            style="Zoom.Vertical.TScale"
        )

        # 数值显示标签
        self.zoom_label = ttk.Label(
            self.float_zoom_frame,
            text="100%",
            font=('Arial', 8),
            background='white'
        )

        # 布局组件
        self.zoom_label.pack(side=tk.TOP, pady=2)
        self.zoom_slider.pack(side=tk.TOP, padx=5, pady=5)

        # 绑定事件
        self.zoom_slider.bind("<ButtonRelease-1>", self._finalize_zoom)

    def _on_zoom_slide(self, value):
        """滑动条实时更新处理"""
        try:
            factor = float(value)
            current_project = self.get_current_project()
            if current_project:
                # 更新显示数值
                self.zoom_label.config(text=f"{int(factor * 100)}%")
                # 应用实时缩放（可根据性能需求节流）
                current_project.canvas.zoom_abs(factor)
        except ValueError:
            pass

    def _finalize_zoom(self, event):
        """滑动结束精度校正"""
        current_value = self.zoom_slider.get()
        rounded_value = round(current_value * 100) / 100.0  # 步进0.01
        self.zoom_slider.set(rounded_value)
        self.zoom_label.config(text=f"{int(rounded_value * 100)}%")

    def on_zoom_changed_by_mousewheel(self):
        self._update_zoom_controls()

    def _update_zoom_controls(self, event=None):
        """更新控件位置和状态"""
        if len(self.list_project_pages) > 0:
            # 计算动态位置
            parent_width = self.frame_notebook.winfo_width()
            parent_height = self.frame_notebook.winfo_height()
            margin = max(10, int(parent_width * 0.03))

            self.float_zoom_frame.place(
                relx=1.0,
                rely=1.0,
                anchor="se",
                x=-margin,
                y=-margin
            )

            # 同步当前项目的缩放状态
            current_project = self.get_current_project()
            if current_project:
                self.zoom_slider.set(current_project.canvas.scale_factor_abs)
                self.zoom_label.config(text=f"{int(current_project.canvas.scale_factor_abs * 100)}%")
        else:
            self.float_zoom_frame.place_forget()

    def get_current_project(self):
        if self.current_tab_index>=0:
            return self.list_project_pages[self.current_tab_index]
        else:
            return None
    #def init_floating_zoom_buttons(self, parent):
    #    """在frame_notebook上创建悬浮控制栏"""
    #    # 创建透明容器Frame
    #    self.float_btn_frame = ttk.Frame(parent)
    #    self.float_btn_frame.place_forget()
    #    #self.float_btn_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # 右下角10px边距
#
    #    # 创建缩放按钮
    #    style = ttk.Style()
    #    style.configure("Floating.TButton",
    #                    padding=6,
    #                    relief="flat",
    #                    width=2)
#
    #    self.zoom_in_btn = ttk.Button(
    #        self.float_btn_frame,
    #        text="+",
    #        style="Floating.TButton",
    #        command=self.zoom_in
    #    )
    #    self.zoom_out_btn = ttk.Button(
    #        self.float_btn_frame,
    #        text="-",
    #        style="Floating.TButton",
    #        command=self.zoom_out
    #    )
#
    #    # 布局按钮
    #    self.zoom_in_btn.pack(side=tk.TOP, pady=2)
    #    self.zoom_out_btn.pack(side=tk.TOP, pady=2)
#
    #    # 绑定Notebook切换事件
    #    self.notebook.bind("<<NotebookTabChanged>>", self.update_floating_zoom_buttons_position)
#
    #    # 初始定位
    #    self.update_floating_zoom_buttons_position()
#
    #def update_floating_zoom_buttons_position(self, event=None):
    #    """动态更新悬浮按钮位置"""
    #    if len(self.list_project_pages) == 0:
    #        return  # 无项目时跳过
    #    # 等待布局计算完成
    #    self.frame_notebook.update_idletasks()
#
    #    # 保持右下角定位
    #    self.float_btn_frame.place_configure(
    #        relx=1.0,
    #        rely=1.0,
    #        anchor="se",
    #        x=-25,
    #        y=-22
    #    )
#
    #def update_floating_zoom_buttons_visibility(self):
    #    """根据项目存在状态更新按钮可见性"""
    #    if len(self.list_project_pages) > 0:
    #        self.float_btn_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    #        self.update_floating_zoom_buttons_position()
    #    else:
    #        self.float_btn_frame.place_forget()
    #def zoom_in(self):
    #    self.list_project_pages[self.current_tab_index].zoom(1.1)
#
    #def zoom_out(self):
    #    self.list_project_pages[self.current_tab_index].zoom(0.9)
#
    def on_notebook_clicked(self, event):
        tab_id = self.notebook.identify(event.x, event.y)
        if "label" in tab_id:
            index = self.notebook.index(f"@{event.x},{event.y}")

            # 銷毀已存在的輸入框
            if self.edit_tab_text:
                self.edit_tab_text.destroy()

            # 獲取標籤的位置和文字
          #  tab_rect = self.notebook.tab(index, "text")
          #  x, y, width, height = self.notebook.tab(index)["image"]  # 獲取標籤位置（需根據實際調整）


            # 創建輸入框並定位到標籤位置
            entry = ttk.Entry(self.notebook, width=10)
            entry.place(x=event.x, y=event.y, anchor="nw")  # 更精確的位置需要計算
            #entry.insert(0, self.notebook.tab(index, "text"))
            entry.insert(0, self.list_project_pages[index].project.name)
            entry.focus()

            # 綁定 Enter 鍵確認修改
            entry.bind("<Return>", lambda e: self.update_tab_text(index, entry.get()))
            # 綁定焦點離開時也確認修改
            entry.bind("<FocusOut>", lambda e: self.update_tab_text(index, entry.get()))

            self.edit_tab_text = entry

    def update_tab_text(self, index, new_text):
        # 更新標籤文字並銷毀輸入框
        self.list_project_pages[index].project.set_name(new_text)
        filename, ext = get_filename_ext(self.list_project_pages[index].project.project_file_path)
        self.notebook.tab(index, text=new_text+'-'+filename)
        self.edit_tab_text.destroy()
        self.edit_tab_text = None

    def add_tab_text_dot(self, index, color):
        color_markers = {
            'red': ' 🔴',
            'blue': ' 🔵',
            'green': ' 🟢',
            'orange': ' 🟠',
            'purple': ' 🟣',
            'black': ' ⚫'
        }
        marker = color_markers.get(color, '')
        tab_text = self.notebook.tab(index, "text")
        tail = tab_text[-2:]
        if tail not in color_markers.values():
            tab_text += marker
            self.notebook.tab(index, text=tab_text)


    def on_tab_changed(self, event):
        # 获取当前选中的标签页索引
        if self.notebook.select():
            self.current_tab_index = self.notebook.index(self.notebook.select())
            self._update_zoom_controls()
            project_page = self.list_project_pages[self.current_tab_index]
            if self.editor_variables:
                self.editor_variables.destroy()
            self.editor_variables = None
            node_key = project_page.current_node_key
            if node_key:
                node = project_page.project.controller_node_graphic.get_node_by_key(node_key)
                self.node_configer.set_node(node=node, project_page=project_page)
            else:
                self.node_configer.destroy()
            self.update_file_menu_button()
           # self.on_node_clicked()

    def on_node_changed(self, node: WORK_NODE):
        self.list_project_pages[self.current_tab_index].update_current_node(node)
        self.add_tab_text_dot(self.current_tab_index, 'red')

    def on_name_changed(self, node: WORK_NODE):
        self.list_project_pages[self.current_tab_index].change_current_node_key(node.key)

    def on_node_clicked(self):
        project_page = self.list_project_pages[self.current_tab_index]
        node_key = project_page.current_node_key
        node = project_page.project.controller_node_graphic.get_node_by_key(node_key)
        self.node_configer.set_node(node=node, project_page=project_page)
        #print("on_node_clicked")
        self.edit_menu.entryconfigure(0, state=tk.NORMAL)
        self.edit_menu.entryconfigure(1, state=tk.NORMAL)
        #self.frame_notebook.focus_force()

    def on_node_deleted(self):
        self.node_configer.clear()
        self.edit_menu.entryconfigure(0, state=tk.DISABLED)
        self.edit_menu.entryconfigure(1, state=tk.DISABLED)

    def on_project_changed(self):
        #self.file_menu.entryconfigure(2, state=tk.NORMAL)
        #self.file_menu.entryconfigure(3, state=tk.NORMAL)
        #self.file_menu.entryconfigure(6, state=tk.NORMAL)

        self.update_file_menu_button()

    def init_node_palette(self):
        # 节点分类颜色配置

        for category, enum_nodes in self.enum_node_categories.items():

            frame = ttk.LabelFrame(self.frame_node_palette, text=category,
                                   style=f"Primary.TLabelframe",
                                  # style=f"{category}.TLabelframe",
                                   )
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            for enum_node in enum_nodes:
                btn = ttk.Button(frame, text= self.get_translation( enum_node.value),
                                 style= f"{category}.TButton",
                               command=lambda nt=enum_node: self.on_node_palette_clicked(nt),
                                 state="disabled",
                                 )
                btn.pack(fill=tk.X, padx=2, pady=2)
                self.list_palette_button.append(btn)

    def on_node_palette_clicked(self, enum_node: ENUM_NODE):
        self.list_project_pages[self.current_tab_index].enum_node_to_insert = enum_node
        self.list_project_pages[self.current_tab_index].enum_canvas_operation = ENUM_CANVAS_OPERATION.ADD_NODE

    def new_project(self):
        tab = ttk.Frame(self.notebook)
        project_name = self.project_name_manager.get_new_name(name = self.get_translation("project"))
        project_page = PROJECT_PAGE(parent=tab, callback_on_node_clicked= self.on_node_clicked, callback_on_changed=self.on_project_changed,
                                    callback_on_zoom_changed=self.on_zoom_changed_by_mousewheel, callback_on_node_deleted=self.on_node_deleted,
                                    name=project_name)
        #project_page.project.llms_api=self.settings.llms_api
        #project_page.project.knowledge_collections=self.settings.knowledge_collections
        project_page.project.is_changed=True
        self.project_name_manager.add_name(project_page.project.name)

        self.notebook.add(tab, text=project_page.project.name)
        self.add_tab_text_dot(self.current_tab_index, 'red')
        self.current_tab_index = len(self.list_project_pages)
        self.list_project_pages.append(project_page)
        self.notebook.select(self.current_tab_index)
        self.file_menu.entryconfigure(2, state=tk.NORMAL)
        self.file_menu.entryconfigure(3, state=tk.NORMAL)
        self.file_menu.entryconfigure(4, state= tk.NORMAL)
        self.file_menu.entryconfigure(5, state=tk.NORMAL)
        self.file_menu.entryconfigure(7, state=tk.NORMAL)
        self.save_button.configure(state=tk.NORMAL)
        self.save_all_button.configure(state=tk.NORMAL)
        self.save_as_button.configure(state=tk.NORMAL)
        self.print_button.configure(state=tk.NORMAL)
        self.close_button.configure(state=tk.NORMAL)
        self.enable_insert_menu(True)
        self.enable_edit_menu(True,4)
        self.enable_debug_menu(True)
        self.enable_pallet_buttons(True)
        #self.update_floating_zoom_buttons_visibility()
        self.close_editors()
        if self.node_configer:
            self.node_configer.destroy()
    
    def open_project(self):
        file_path = filedialog.askopenfilename(filetypes=[(self.get_translation("wofa_projects"), "*."+PROJECT_FILE_EXT)])
        if file_path:
            project = WORKFLOW_PROJECT.from_file(file_path, self.settings.knowledge_collections)
            self.project_name_manager.add_name(project.name)
            tab = ttk.Frame(self.notebook)
            project_page = PROJECT_PAGE(parent = tab, project=project, callback_on_node_clicked=self.on_node_clicked, callback_on_node_deleted=self.on_node_deleted,
                                        callback_on_changed=self.on_project_changed,callback_on_zoom_changed=self.on_zoom_changed_by_mousewheel,)
           # project_page.project.workflow.llms_api = self.settings.llms_api
           # project_page.project.workflow.knowledge_collections = self.settings.knowledge_collections
            filename, ext = get_filename_ext(file_path)
            self.notebook.add(tab, text=project_page.project.name+"-"+ filename)
            self.current_tab_index = len(self.list_project_pages)
            self.notebook.select(self.current_tab_index)

            project_page.redraw_canvas()
            self.list_project_pages.append(project_page)

            self.file_menu.entryconfigure(4, state=tk.NORMAL)
            self.file_menu.entryconfigure(5, state=tk.NORMAL)
            self.file_menu.entryconfig(7, state=tk.NORMAL)
            self.save_as_button.configure(state=tk.NORMAL)
            self.print_button.configure(state=tk.NORMAL)
            self.close_button.configure(state=tk.NORMAL)
            self.enable_insert_menu(True)
            self.enable_edit_menu(True, 4)
            self.enable_debug_menu(True)
            self.enable_pallet_buttons(True)
            # self.update_floating_zoom_buttons_visibility()
            self.close_editors()
            if self.node_configer:
                self.node_configer.destroy()
            #if project.is_changed:
            #    self.update_file_menu_button()


    def save_project(self):
        if self.current_tab_index>=0 :
            project = self.list_project_pages[self.current_tab_index].project
            self._save_project(self.current_tab_index, project)
            #self.update_save_all_menu_button()
            self.update_file_menu_button()


    def _save_project(self, index: int, project:WORKFLOW_PROJECT):
        filepath = project.project_file_path
        if not is_string_valid(filepath):
            filepath = filedialog.asksaveasfilename(
                title= self.get_translation("save") + self.get_translation("wofa_projects"),
                filetypes=[(self.get_translation("wofa_projects"), "*."+PROJECT_FILE_EXT)],
                defaultextension="."+PROJECT_FILE_EXT
            )
            if filepath:
                # 手動確保副檔名正確
                root, ext = os.path.splitext(filepath)
                if ext.lower() != "."+PROJECT_FILE_EXT:
                    filepath = root + "."+PROJECT_FILE_EXT

        if is_string_valid(filepath):
            self.list_project_pages[index].project.set_project_file_path(filepath)
            filename, ext = get_filename_ext(filepath)
            self.notebook.tab(index, text=self.list_project_pages[index].project.name + "-" + filename)
            self.list_project_pages[index].project.to_file()
            self.list_project_pages[index].project.is_changed=False

    def save_all_projects(self):
        for index, project_page in enumerate(self.list_project_pages):
            self._save_project(index, project_page.project)

        self.update_file_menu_button()

    def save_project_as(self):
        if self.current_tab_index >= 0:
            filepath = filedialog.asksaveasfilename(
                title=self.get_translation("save_as") + self.get_translation("wofa_projects"),
                filetypes=[("WOFA Projects", "*." + PROJECT_FILE_EXT)],
                defaultextension="."+PROJECT_FILE_EXT
            )
            if filepath:
                # 手動確保副檔名正確
                root, ext = os.path.splitext(filepath)
                if ext.lower() != "." + PROJECT_FILE_EXT:
                    filepath = root + "." + PROJECT_FILE_EXT
            if is_string_valid(filepath):
                self.list_project_pages[self.current_tab_index].project.set_project_file_path(filepath)

            self.list_project_pages[self.current_tab_index].project.to_file()
            filename, ext = get_filename_ext(filepath)
            self.notebook.tab(self.current_tab_index, text=self.list_project_pages[
                                                               self.current_tab_index].project.name + "-" + filename)
            self.update_file_menu_button()

    def print_project(self):
        self.list_project_pages[self.current_tab_index].canvas.print()
        # 创建临时 PostScript 文件
        #ps_file = tempfile.NamedTemporaryFile(suffix='.ps', delete=False)
        #ps_file.close()

        # 将 Canvas 导出为 PostScript
        #self.list_project_pages[self.current_tab_index].canvas.postscript(file=ps_file.name, colormode='color')

        # 方法 1: 使用系统默认程序打印
       #try:
       #    # Windows
       #    os.startfile(ps_file.name, "print")
       #except Exception as e:
       #    print("Windows 列印錯誤:", e)
       #    # macOS/Linux
       #    try:
       #        subprocess.run(["lpr", ps_file.name])
       #    except Exception as e:
       #        print("无法自动打印，请手动打印文件:", ps_file.name)

        # 方法 2: 转换为 PDF 再打印 (使用 Ghostscript)
        # 需要安装 Ghostscript: https://www.ghostscript.com/
        #try:
        #    pdf_file = ps_file.name.replace('.ps', '.pdf')
        #    subprocess.run(["ps2pdf", ps_file.name, pdf_file])
        #    os.startfile(pdf_file, "print")
        #except:
        #    print("Ghostscript 未安装，无法转换为 PDF")

    def close_editors(self):
        #if self.configer_schedule:
        #    self.configer_schedule.destroy()
        #    self.configer_schedule = None

        if self.viewer_variables:
            self.viewer_variables .destroy()
            self.viewer_variables = None

        if self.editor_variables:
            self.editor_variables .destroy()
            self.editor_variables = None

        if self.editor_llms_api:
            self.editor_llms_api.destroy()
            self.editor_llms_api = None

        if self.picker_knowledge_collections    :
            self.picker_knowledge_collections .destroy()
            self.picker_knowledge_collections = None

    def close_project(self):
        # 检查未保存修改
        if self.check_unsaved_changes():
            return

        if self.current_tab_index >= 0:
            self.list_project_pages.pop(self.current_tab_index)
            self.notebook.forget(self.current_tab_index)
            self.close_editors()

            if len(self.list_project_pages) == 0:
                self.current_tab_index = -1
                self.enable_pallet_buttons(False)
                self.enable_insert_menu(False)
                self.enable_edit_menu(False)
                self.enable_debug_menu(False)
                self.file_menu.entryconfigure(2, state=tk.DISABLED)
                self.file_menu.entryconfigure(3, state=tk.DISABLED)
                self.file_menu.entryconfigure(4, state=tk.DISABLED)
                self.file_menu.entryconfigure(5, state=tk.DISABLED)
                self.file_menu.entryconfigure(7, state=tk.DISABLED)

            elif self.current_tab_index == len(self.list_project_pages):
                self.current_tab_index -= 1
        self.update_file_menu_button()

        if self.current_tab_index>=0:
            node_graphic = self.list_project_pages[self.current_tab_index].get_current_node_graphic()
            if node_graphic:
                self.node_configer.set_node(node_graphic.node, self.list_project_pages[self.current_tab_index])
        elif self.node_configer:
            self.node_configer.destroy()
       # self.update_floating_zoom_buttons_visibility()
    
    def check_unsaved_changes(self):
        # 检查项目是否有未保存的修改
        if self.current_tab_index>=0 and self.list_project_pages[self.current_tab_index].project.is_changed:
            return messagebox.askyesnocancel(self.get_translation("unsaved_changes"),
                                           self.get_translation("save_before_closing"))
        return False

    def update_file_menu_button(self):
        if self.current_tab_index >= 0:
            self.file_menu.entryconfigure(4, state=tk.NORMAL)
            self.file_menu.entryconfigure(5, state=tk.NORMAL)
            self.file_menu.entryconfigure(7, state=tk.NORMAL)
            self.save_as_button.configure(state=tk.NORMAL)
            self.print_button.configure(state=tk.NORMAL)
            self.close_button.configure(state=tk.NORMAL)
        else:
            self.file_menu.entryconfigure(4, state=tk.DISABLED)
            self.file_menu.entryconfigure(5, state=tk.DISABLED)
            self.file_menu.entryconfigure(7, state=tk.DISABLED)
            self.save_as_button.configure(state=tk.DISABLED)
            self.print_button.configure(state=tk.DISABLED)
            self.close_button.configure(state=tk.DISABLED)

        #self.add_tab_text_dot(self.current_tab_index, 'red')
        self.update_save_menu_button()
        self.update_save_all_menu_button()

    def update_save_menu_button(self):
        self.file_menu.entryconfigure(2, state=tk.DISABLED)
        self.save_button.configure(state=tk.DISABLED)

        if self.current_tab_index>=0:
            is_changed = self.list_project_pages[self.current_tab_index].project.is_changed

            if is_changed:
                self.file_menu.entryconfigure(2, state=tk.NORMAL)
                self.save_button.configure(state=tk.NORMAL)
                self.add_tab_text_dot(self.current_tab_index, 'red')


    def update_save_all_menu_button(self):
        is_changed = False
        if self.list_project_pages and len(self.list_project_pages)>0:
            is_changed = self.list_project_pages[0].project.is_changed
            if not is_changed and len(self.list_project_pages)>1:
                for i in range(1, len(self.list_project_pages)):
                    is_changed = is_changed or self.list_project_pages[i].project.is_changed
                    if is_changed:
                        break

        if is_changed:
            self.file_menu.entryconfigure(3, state=tk.NORMAL)
            self.save_all_button.configure(state=tk.NORMAL)
            self.add_tab_text_dot(self.current_tab_index, 'red')
            #self.close_button.configure(state=tk.NORMAL)
        else:
            self.file_menu.entryconfigure(3, state=tk.DISABLED)
            self.save_all_button.configure(state=tk.DISABLED)
            #self.close_button.configure(state=tk.DISABLED)

    def on_settings_llms_api_changed(self, llms_api: LLMS_API):
        self.settings.llms_api = llms_api
        self.settings.save()

    def edit_settings_llms_api(self):
        #if len(self.list_project_pages) > 0:
            if self.editor_settings_llms_api:
                self.editor_settings_llms_api.lift()
            else:
                self.editor_settings_llms_api = Editor_LLMS_API(parent=self.root,
                                                                callback= self.on_settings_llms_api_changed,
                                                                llms_api=self.settings.llms_api, translator=self.translator)
        #else:
        #    messagebox.showwarning("警告", "必須有打開的專案！")

    def on_settings_knowledge_collections_changed(self, items: KNOWLEDGE_COLLECTIONS):
        self.settings.knowledge_collections = items
        self.settings.save()

    def edit_settings_knowledge_collections(self):
        if self.editor_settings_knowledge_collections:
            self.editor_settings_knowledge_collections.lift()
        else:
            self.editor_settings_knowledge_collections=Editor_KNOWLEDGE_COLLECTIONS(parent=self.root, callback=self.on_settings_knowledge_collections_changed,
                               items=self.settings.knowledge_collections, translator=self.translator)

    def on_llms_api_changed(self, llms_api: LLMS_API):
        self.list_project_pages[self.current_tab_index].project.llms_api = llms_api
        self.list_project_pages[self.current_tab_index].project.is_changed=True

        self.add_tab_text_dot(self.current_tab_index, 'red')
        self.update_save_menu_button()
        self.update_save_all_menu_button()
        if self.node_configer and self.node_configer.node:
            #self.node_configer.set_llms_api(llms_api=llms_api)
            self.node_configer.refresh()

    def edit_llms_api(self):
        # if len(self.list_project_pages) > 0:
        if self.editor_llms_api:
            self.editor_llms_api.lift()
        else:
            self.editor_llms_api = Editor_LLMS_API(parent=self.root,
                                                   callback=self.on_llms_api_changed,
                                                   callback_settings=self.on_settings_llms_api_changed,
                        llms_api= self.list_project_pages[self.current_tab_index].project.llms_api ,
                        settings_llms_api=self.settings.llms_api,
                        translator=self.translator)

        # else:
        #    messagebox.showwarning("警告", "必須有打開的專案！")

    def on_list_knowledge_collection_changed(self, list_item: [KNOWLEDGE_COLLECTION]):
        self.list_project_pages[self.current_tab_index].project.knowledge_collections.set_list_item(list_item)

        self.list_project_pages[self.current_tab_index].project.is_changed = True
        self.add_tab_text_dot(self.current_tab_index, 'red')
        self.update_save_menu_button()
        self.update_save_all_menu_button()
        if self.node_configer:
            self.node_configer.refresh()

    #def edit_knowledge_collections(self):
    #    if self.editor_knowledge_collections:
    #        self.editor_knowledge_collections.lift()
    #    else:
    #        self.editor_knowledge_collections = Editor_KNOWLEDGE_COLLECTIONS(parent=self.root, callback=self.on_knowledge_collections_changed,
    #                                                                         items=self.list_project_pages[self.current_tab_index].project.knowledge_collections,
    #                                                                         settings_knowledge_collections=self.settings.knowledge_collections,
    #                                                                         translator=self.translator)
   # def on_mount_manager_changed(self, mount_manager: MountManager):
   #     self.list_project_pages[
   #         self.current_tab_index].project.mount_manager = mount_manager
   #     self.list_project_pages[self.current_tab_index].project.is_changed = True
   #     self.list_project_pages[self.current_tab_index].refresh()
#
  # def edit_mount_manager(self):
  #     if self.editor_mount_manager:
  #         self.editor_mount_manager.lift()
  #     else:
  #         self.editor_mount_manager = Editor_MOUNT_MANAGER(parent=self.root,
  #                                                          mount_manager=self.list_project_pages[
  #                                                                              self.current_tab_index].project.mount_manager,
  #                                                          callback=self.on_mount_manager_changed,
  #                                                          translator=self.translator)
    def pick_knowledge_collections(self):
        if self.picker_knowledge_collections:
            self.picker_knowledge_collections.lift()
        else:
            self.picker_knowledge_collections = Picker_KNOWLEDGE_COLLECTIONS(parent=self.root,
                                                                             callback=self.on_list_knowledge_collection_changed,
                                                                             callback_settings=self.on_settings_knowledge_collections_changed,
                                                                             items=self.list_project_pages[
                                                                                 self.current_tab_index].project.knowledge_collections,
                                                                             settings_knowledge_collections=self.settings.knowledge_collections,
                                                                             translator=self.translator)


    def on_variables_changed(self, variables: VARIABLES):
        self.list_project_pages[self.current_tab_index].project.global_variables = variables
        self.list_project_pages[self.current_tab_index].project.is_changed = True
        self.list_project_pages[self.current_tab_index].refresh()
        self.add_tab_text_dot(self.current_tab_index, 'red')
        self.update_save_menu_button()
        self.update_save_all_menu_button()
        if self.node_configer and self.node_configer.node:
            self.node_configer.refresh()

    #def on_server_url_changed(self, server_url: str):
    #    self.list_project_pages[self.current_tab_index].project.server_url = server_url
    #    self.list_project_pages[self.current_tab_index].project.is_changed = True
    #    self.list_project_pages[self.current_tab_index].refresh()
    #    self.update_save_menu_button()
    #    self.update_save_all_menu_button()
    #    if self.node_configer:
    #        self.node_configer.refresh()

    def edit_cut(self):
        project_page = cast(PROJECT_PAGE, self.list_project_pages[self.current_tab_index])
        self.node_graphic_tmp =  project_page.get_current_node_graphic()
        self.node_graphic_tmp.node.reset_list_next_node_key()
        self.node_graphic_tmp.graphic.reset_list_output_knot()
        if self.node_graphic_tmp:
            project_page.delete_node_graphic(self.node_graphic_tmp)
            self.edit_menu.entryconfigure(0, state=tk.DISABLED)
            self.edit_menu.entryconfigure(2, state=tk.NORMAL)

    def edit_copy(self):
        project_page = cast(PROJECT_PAGE, self.list_project_pages[self.current_tab_index])
        self.node_graphic_tmp = project_page.get_current_node_graphic()
        self.node_graphic_tmp.node.reset_list_next_node_key()
        self.node_graphic_tmp.graphic.reset_list_output_knot()
        self.edit_menu.entryconfigure(2, state=tk.NORMAL)

    def edit_paste(self):
        project_page = cast(PROJECT_PAGE, self.list_project_pages[self.current_tab_index])
        project_page.insert_node_graphic(self.node_graphic_tmp)
        self.edit_menu.entryconfigure(2, state=tk.NORMAL)

    def edit_variables(self):
        if len(self.list_project_pages) > 0:
            if self.editor_variables:
                self.editor_variables.lift()
            else:
                self.editor_variables = Editor_VARIABLES(parent=self.root, callback=self.on_variables_changed,
                         variables=self.list_project_pages[self.current_tab_index].project.global_variables, translator=self.translator)
        else:
            messagebox.showwarning(self.get_translation("warning"), self.get_translation("must_have_opened_project"))

    def view_variables(self):
        if len(self.list_project_pages) > 0:
            if self.viewer_variables:
                self.viewer_variables.lift()
            else:
                self.viewer_variables = Viewer_VARIABLES(parent=self.root,
                                                    variables=self.list_project_pages[self.current_tab_index].project.global_variables,
                                                    translator=self.translator)
        else:
            messagebox.showwarning(self.get_translation("warning"), self.get_translation("must_have_opened_project"))

    def close_viewer_variables(self):
        if self.viewer_variables:
            self.viewer_variables.destroy()

    def close_editor_variables(self):
        if self.editor_variables:
            self.editor_variables.destroy()

    #def edit_server_url(self):
    #    if len(self.list_project_pages) > 0:
    #        self.editor_server_url = Editor_LINE(
    #            parent=self.root,
    #            label="server_url",
    #            value=self.list_project_pages[self.current_tab_index].project.server_url,
    #            callback=self.on_server_url_changed,
    #            translator=self.translator)
    #    else:
    #        messagebox.showwarning(self.get_translation("warning"), self.get_translation("must_have_opened_project"))

    #def close_editor_server_url(self):
    #    if self.editor_server_url:
    #        self.editor_server_url.destroy()

    #def on_schedule_changed(self, schedule_time: SCHEDULE_TIME):
    #    self.list_project_pages[self.current_tab_index].project.schedule_time = schedule_time
    #    self.list_project_pages[self.current_tab_index].project.is_changed = True
    #    self.update_save_menu_button()
    #    self.update_save_all_menu_button()

    #def edit_schedule(self):
    #    if len(self.list_project_pages) > 0:
    #        if self.configer_schedule:
    #            self.configer_schedule.lift()
    #        else:
    #            self.configer_schedule =  Configer_SCHEDULE_TIME(parent=self.root, callback=self.on_schedule_changed,
    #                               schedule_time=self.list_project_pages[self.current_tab_index].project.schedule_time, translator=self.translator)
    #    else:
    #        messagebox.showwarning(self.get_translation("warning"), self.get_translation("must_have_opened_project"))
#
    # 以下是运行调试功能 -------------------------------------------------

    def init_workflow_for_debug(self):
        project_page = self.list_project_pages[self.current_tab_index]
        workflow = project_page.project.workflow
        if project_page.current_node_key:
            current_node_key = project_page.current_node_key
        else:
            current_node_key = workflow.start_node_key

        workflow.set_current_node_key(current_node_key )
        workflow.set_callback_current_node_changed(
            project_page.on_current_node_changed
        )

        #current_node_graphic = project_page.project.controller_node_graphic.get_node_graphic_by_key(current_node_key)
        #if current_node_graphic.node.enum_node in [ENUM_NODE.NODE_ASK_LLM, ENUM_NODE.NODE_CATEGORIZED_BY_LLM,
        #                           ENUM_NODE.NODE_ASK_LLM_WITH_KNOWLEDGE,
        #                           ENUM_NODE.NODE_KNOWLEDGE_RETRIEVER, ENUM_NODE.NODE_TRANSLATED_BY_LLM]:
        #    current_node_graphic.node.set_llms_api(project_page.project.llms_api)
        #    project_page.update_node_graphic(current_node_graphic)
#
        project_page.project.workflow = workflow
        self.list_project_pages[self.current_tab_index] = project_page



    def run(self):
        if self.current_tab_index>=0:
            self.view_variables()
            self.list_project_pages[self.current_tab_index].enum_run_type= ENUM_RUN_TYPE.RUN
            self.init_workflow_for_debug()
            self.list_project_pages[self.current_tab_index].project.workflow(enum_run_type=ENUM_RUN_TYPE.RUN)
            self.viewer_variables.refresh()

    
    def step_run(self):
        # 步进执行逻辑
        if self.current_tab_index >= 0:
            self.view_variables()
            self.init_workflow_for_debug()
            self.list_project_pages[self.current_tab_index].project.workflow(enum_run_type=ENUM_RUN_TYPE.STEP)
            self.viewer_variables.refresh()


    def single_node_run(self):
        # 步进执行逻辑
        if self.current_tab_index >= 0:
            self.view_variables()
            self.init_workflow_for_debug()
            self.list_project_pages[self.current_tab_index].project.workflow(enum_run_type=ENUM_RUN_TYPE.SINGLE)
            self.viewer_variables.refresh()

    def stop_run(self):
        if self.current_tab_index >= 0:
            self.list_project_pages[self.current_tab_index].project.workflow.stop_run()
            self.viewer_variables.destroy()

    #ef check_activation(self):
    #   """检查是否已经激活"""
    #   # 这里可以添加更复杂的验证逻辑，如检查注册表或文件
    #   return os.path.exists("settings.json")

    #ef show_activation_dialog(self):
    #   """显示激活对话框"""
    #   dialog = tk.Toplevel()
    #   dialog.title(self.translator.get_translation("product_activation"))
    #   dialog.geometry("400x250")
    #   dialog.grab_set()  # 模态对话框

    #   # 感谢购买标签
    #   tk.Label(dialog, text=self.translator.get_translation("appreciation_purchase"), font=("Arial", 16)).pack(pady=10)

    #   # 序列号输入
    #   tk.Label(dialog, text=self.translator.get_translation("product_serial_no")).pack(pady=(10, 0))
    #   serial_entry = tk.Entry(dialog, width=30)
    #   serial_entry.pack()

    #   # 公司名称输入
    #   tk.Label(dialog, text=self.translator.get_translation("user_company")).pack(pady=(10, 0))
    #   company_entry = tk.Entry(dialog, width=30)
    #   company_entry.pack()

    #   def on_button_register_clicked():
    #       self.serial_no = serial_entry.get().strip()
    #       self.user_company = company_entry.get().strip()
    #       if not self.serial_no or not self.user_company:
    #           messagebox.showerror("错误", "请输入序列号和公司名称")
    #           return

    #       if self.send_activation(self.serial_no, self.user_company):
    #           with open("activated.flag", "w") as f:
    #               f.write("activated")
    #           messagebox.showinfo("成功", "产品激活成功！")
    #           dialog.destroy()
    #           self.is_activated=True
    #       else:
    #           messagebox.showerror("错误", "激活失败，请检查网络或联系供应商")
    #           self.is_activated= False

    #   tk.Button(dialog, text=self.translator.get_translation("activate_product"), command=on_button_register_clicked, width=15).pack(pady=20)

    #ef send_activation(self, serial, company):
    #   """发送激活信息到服务器"""
    #   try:
    #       response = requests.post(
    #           "https://syntak.net/wofa/activation.php",
    #           data={
    #               'product_serial': serial,
    #               'user_company': company
    #           },
    #           timeout=10
    #       )
    #       return response.status_code == 200 and response.text.strip() == "SUCCESS"
    #   except Exception as e:
    #       print(f"激活错误: {e}")
    #       return False

from pathlib import Path

class Settings:
    def __init__(self, file_path: str = "settings.json"):
        """
        初始化設定類
        :param file_path: 設定檔路徑 (預設為 settings.json)
        """
        self.file_path = file_path
        self.settings = {}
        self.llms_api = LLMS_API()
        self.knowledge_collections = KNOWLEDGE_COLLECTIONS()
        self._load()

    def _load(self) -> None:
        """從檔案載入設定"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "settings" in data:
                        self.settings = data['settings']
                    if "llms_api" in data:
                        llms_api = LLMS_API.from_dict(data['llms_api'])
                        if llms_api:
                            self.llms_api = llms_api
                    if "knowledge_collections" in data:
                        knowledge_collections= KNOWLEDGE_COLLECTIONS.from_dict( data['knowledge_collections'])
                        if knowledge_collections:
                            self.knowledge_collections=knowledge_collections

        except (json.JSONDecodeError, IOError) as e:
            print(f"載入設定檔失敗: {e}")
            self.settings = {}

    def save(self) -> None:
        data={"settings":self.settings,
              "llms_api": self.llms_api.to_dict(),
              "knowledge_collections":self.knowledge_collections.to_dict()}
        """儲存設定到檔案"""
        try:
            # 確保目錄存在
            file_path = Path(self.file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"儲存設定檔失敗: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        獲取設定值
        :param key: 設定鍵
        :param default: 如果鍵不存在時返回的預設值
        :return: 設定值或預設值
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        設定值並立即保存
        :param key: 設定鍵
        :param value: 要設定的值
        """
        self.settings[key] = value
        self.save()

    def remove(self, key: str) -> None:
        """
        移除設定並立即保存
        :param key: 要移除的設定鍵
        """
        if key in self.settings:
            del self.settings[key]
            self.save()

    def get_all(self) -> dict:
        """獲取所有設定"""
        return self.settings.copy()

def show_error_dialog(title, message):
    """显示错误对话框"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception as e:
        print(f"无法显示错误对话框: {str(e)}")
        print(f"原始错误: {title} - {message}")

#def show_error_dialog(title, message):
#    """显示错误对话框"""
#    try:
#        import tkinter as tk
#        from tkinter import messagebox
#        root = tk.Tk()
#        root.withdraw()
#        messagebox.showerror(title, message)
#    except Exception as e:
#        print(f"无法显示错误对话框: {str(e)}")
#        print(f"原始错误: {title} - {message}")


#def excepthook(exc_type, exc_value, exc_traceback):
#    """全局异常处理"""
#    error_msg = f"未捕获的异常: {exc_type.__name__}: {exc_value}"
#
#    # 记录到日志文件
#    try:
#        import logging
#        logging.basicConfig(
#            filename='wofa_ide_error.log',
#            level=logging.ERROR,
#            format='%(asctime)s - %(levelname)s - %(message)s'
#        )
#        logging.error(error_msg, exc_info=(exc_type, exc_value, exc_traceback))
#    except:
#        pass
#
#    # 显示错误信息
#    traceback_details = "\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
#    error_display = f"程序发生严重错误:\n\n{str(exc_value)}\n\n详细信息已保存到日志文件"
#
#    show_error_dialog("程序错误", error_display)
#    sys.exit(1)
#
#
## 设置全局异常处理
#sys.excepthook = excepthook

def main():
   #os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 解决 OpenMP 冲突
   #os.environ["OMP_NUM_THREADS"] = "1"  # 限制线程数
   #os.environ["OPENBLAS_NUM_THREADS"] = "1"  # 限制 BLAS 线程
   ide = WorkflowIDE()
   ide.root.mainloop()

if __name__ == "__main__":
   main()