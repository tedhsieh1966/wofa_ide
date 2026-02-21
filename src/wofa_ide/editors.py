import sys
from typing import List,  Optional, get_args
import tkinter.font as tkFont
from py_libraries.MathOp import *
from py_libraries.UiOp import *
from py_libraries.TimeOp import *
from py_libraries.StringOp import title
from py_libraries.LanguageOp import LanguageTranslator

from py_workflow.py_workflow import *
#from py_workflow.workflow_base import *
#from py_workflow.workflow_nodes import *
#from py_workflow.workflow_nodes_torch import *

from py_llm_api.LLM_RAG import ENUM_STORAGE_TYPE
from py_llm_api.LLM_OpenAI import *
from py_llm_api.LLM_Gemini import *
from py_llm_api.LLM_Qwen import *
from py_llm_api.LLM_Claude import *
from py_llm_api.LLM_Grok import *
from py_llm_api.LLMS import *

import tempfile
from copy import copy, deepcopy
import os
import subprocess
from PIL import Image, ImageTk, ImageDraw, ImageFont

ARG_ID = 0
ARG_TYPE = 1
ARG_KEY = 2
ARG_NODE_TYPE = 3

DASH_STYLES = {
    "solid": None,          # 实线
    "dashed": (4, 2),       # 普通虚线
    "dotted": (1, 2),       # 点状虚线
    "custom": (8, 3, 2, 3)  # 自定义复杂虚线
}

class Editor:
    def __init__(self):
        self.name = "Test Editor"

    def __str__(self):
        return f"Editor: {self.name}"

def setup_ttk_style():
    ttk.Style().configure(
        "Config_Title.TLabel",  # 自定義樣式名稱（格式：任意名稱.TLabel）
        font="Arial 14",  # 字型
        foreground="blue"  # 文字顏色
    )
    # LabelFrame 样式
    ttk.Style().configure(
        "Primary.TLabelframe",
        background="lightgrey",
        bordercolor="black",
        relief="ridge",
        padding=(10, 5, 10, 10)  # 左, 上, 右, 下
    )
    ttk.Style().configure(
        "Primary.TLabelframe.Label",
        font=('Arial', 10, 'bold'),
        foreground="#336699",
        background="#f0f0f0"
    )
    ttk.Style().configure(
        "Logic.TLabelframe",
        background="lightgrey",
        bordercolor="black",
        relief="ridge",
        padding=(10, 5, 10, 10)  # 左, 上, 右, 下
    )
    ttk.Style().configure(
        "Logic.TLabelframe.Label",
        font=('Arial', 10, 'bold'),
        foreground="#336699",
        background="#f0f0f0"
    )
    ttk.Style().configure(
        "AI.TLabelframe",
        background="yellow",
        bordercolor="black",
        relief="ridge",
        padding=(10, 5, 10, 10)  # 左, 上, 右, 下
    )
    ttk.Style().configure(
        "AI.TLabelframe.Label",
        font=('Arial', 10, 'bold'),
        foreground="#336699",
        background="#f0f0f0"
    )
    ttk.Style().configure(
        "IO.TLabelframe",
        background="pink",
        bordercolor="black",
        relief="ridge",
        padding=(10, 5, 10, 10)  # 左, 上, 右, 下
    )
    ttk.Style().configure(
        "IO.TLabelframe.Label",
        font=('Arial', 10, 'bold'),
        foreground="#336699",
        background="#f0f0f0"
    )

    # Button 样式
    ttk.Style().configure(
        "Primary.TButton",
        foreground="black",
        background="#336699",
        borderwidth=2,
        font=('Arial', 10, 'bold'),
        padding=6
    )
    ttk.Style().map(
        "Primary.TButton",
        foreground=[
            ('pressed', 'black'),
            ('active', 'black'),
            ('disabled', '#cccccc')
        ],
        background=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8'),
            ('disabled', '#a0a0a0')
        ],
        bordercolor=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8')
        ]
    )
    ttk.Style().configure(
        "Logic.TButton",
        foreground="black",
        background="lightgreen",
        borderwidth=2,
        font=('Arial', 10, 'bold'),
        padding=6
    )
    ttk.Style().map(
        "Logic.TButton",
        foreground=[
            ('pressed', 'black'),
            ('active', 'black'),
            ('disabled', '#cccccc')
        ],
        background=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8'),
            ('disabled', '#a0a0a0')
        ],
        bordercolor=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8')
        ]
    )
    ttk.Style().configure(
        "AI.TButton",
        foreground="black",
        background="yellow",
        borderwidth=2,
        font=('Arial', 10, 'bold'),
        padding=6
    )
    ttk.Style().map(
        "AI.TButton",
        foreground=[
            ('pressed', 'black'),
            ('active', 'black'),
            ('disabled', '#cccccc')
        ],
        background=[
            ('pressed', '#254c6b'),
            ('active', 'yellow'),
            ('disabled', '#a0a0a0')
        ],
        bordercolor=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8')
        ],
    )
    ttk.Style().configure(
        "IO.TButton",
        foreground="black",
        background="cyan",
        borderwidth=2,
        font=('Arial', 10, 'bold'),
        padding=6
    )
    ttk.Style().map(
        "IO.TButton",
        foreground=[
            ('pressed', 'black'),
            ('active', 'black'),
            ('disabled', '#cccccc')
        ],
        background=[
            ('pressed', '#254c6b'),
            ('active', 'lightcyan'),
            ('disabled', '#a0a0a0')
        ],
        bordercolor=[
            ('pressed', '#254c6b'),
            ('active', '#4078a8')
        ],
    )
    ttk.Style().configure('Custom.Entry',
                   background='white',   # 背景色
                   foreground='darkgrey',    # 文字颜色
                   fieldbackground='#FFFFCC',  # 输入区域背景
                   bordercolor='black',       # 边框颜色
                   borderwidth=2,           # 边框宽度
                   font=('Arial', 12),      # 字体
                   padding=5)               # 内边距


class ENUM_CANVAS_OPERATION(Enum):
  #  DRAG_ADD = "drag_add"
    DRAG_MOVE = "drag_move"
    DRAG_CONNECT = "drag_connect"
    ADD_NODE= "add_node"
    PAN = "pan"
  #  PRESS_INSERT = "press_insert"


enum_NODE_OPERATION_from_value = {member.value: member for member in ENUM_CANVAS_OPERATION}

def get_enum_NODE_OPERATION_from_value(value)->ENUM_CANVAS_OPERATION:
    return enum_NODE_OPERATION_from_value.get(value)

def destroy_TK_WINDOW(root: TK_WINDOW, is_destroy_root=True):
    if root and root.winfo_exists():
        for widget in root.winfo_children():
            widget.destroy()
        if is_destroy_root:
            root.destroy()
            root = None


class CanvasScrollZoom(tk.Canvas):
    def __init__(self, parent, **kwargs):
        # 初始化基础 Canvas
        super().__init__(parent, **kwargs)

        self.font_cache = {}
        self.default_font = tkFont.Font()  # 默认字体对象
        # 缩放相关属性
        self.scale_factor_abs = 1.0
        self.scale_factor_rel = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.margin = 100.0  # 像素边距阈值
        # 初始化坐标系转换矩阵
        #self.transform_matrix = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        self.callback_on_zoom_changed : Optional[Callable]=None
        # 滚动条配置
        self._setup_scrollbars(parent)

        # 事件绑定
        self._bind_events()
        self._bind_auto_scroll()
        #self.config(width=parent.winfo_width(), height=parent.winfo_height())
        #self.update_idletasks()  # 確保內容渲染完成
        #self.config(scrollregion=self.bbox("all"))  # 自動計算內容邊界

    def set_callback(self, callback:Callable):
        self.callback_on_zoom_changed = callback

    def _setup_scrollbars(self, parent):
        """创建并配置滚动条"""
        # 水平滚动条
        self.xscroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
        self.xscroll.grid(row=1, column=0, sticky="ew")

        # 垂直滚动条
        self.yscroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        self.yscroll.grid(row=0, column=1, sticky="ns")

        # 双向绑定
        self.configure(
            xscrollcommand=self.xscroll.set,
            yscrollcommand=self.yscroll.set
        )

    def _bind_events(self):
        """绑定缩放和滚动事件"""
        # Ctrl+鼠标滚轮缩放
        #self.bind("<Control-MouseWheel>", self._on_zoom)
        self.bind("<MouseWheel>", self._on_zoom)

        # Alt+拖动平移
        #self.bind("<Alt-B1-Motion>", self.on_pan)
        #self.bind("<Alt-Button-1>", self.on_pan_start)

    def _bind_auto_scroll(self):
        """绑定元素变化事件"""
        self.bind("<Configure>", self.update_scroll_region)
        self.bind_all("<ButtonRelease>", self.update_scroll_region)

    def update_scroll_region(self, event=None):
        """带边距检测的滚动区域更新"""
        bbox = self.bbox("all")
        if not bbox:
            return

        # 计算扩展后的边界
        x1, y1, x2, y2 = bbox
        view_x1, view_y1 = self.canvasx(0), self.canvasy(0)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        #print(f"w={w},h={h}")
        view_x2, view_y2 = self.canvasx(self.winfo_screenwidth()), self.canvasy(self.winfo_screenheight())
        #view_x2, view_y2 = self.canvasx(self.winfo_width()), self.canvasy(self.winfo_height())

        # 检测是否需要扩展
        expand_right = (x2 + self.margin > view_x2) and (x2 > view_x2)
        expand_left = (x1 - self.margin < view_x1) and (x1 < view_x1)
        expand_bottom = (y2 + self.margin > view_y2) and (y2 > view_y2)
        expand_top = (y1 - self.margin < view_y1) and (y1 < view_y1)

        # 应用扩展
      # new_bbox = (
      #     x1 - self.margin if expand_left else x1,
      #     y1 - self.margin if expand_top else y1,
      #     x2 + self.margin if expand_right else x2,
      #     y2 + self.margin if expand_bottom else y2
      # )
        new_bbox = (
            min(x1 - self.margin, view_x1) ,
            min(y1 - self.margin, view_y1),
            max(x2 + self.margin, view_x2),
            max(y2 + self.margin, view_y2)
        )

        self.config(scrollregion=new_bbox)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        #print(f"w={w},h={h}")
   #def _update_scrollregion(self):
   #   """更新滚动区域（自动计算内容范围）"""
   #   self.configure(scrollregion=self.bbox("all"))
   #   self.update_idletasks()

    def get_event_coord(self, event):
        raw_x, raw_y = event.x, event.y  # 窗口坐标
        phys_x = self.canvasx(raw_x)  # 物理坐标（考虑滚动）
        phys_y = self.canvasy(raw_y)
        logic_x, logic_y = self.physical_to_logical(phys_x, phys_y)  # 逻辑坐标（包含缩放）
        return logic_x, logic_y
    # 以下是坐标转换核心方法
    def logical_to_physical(self, x, y):
        """逻辑坐标 → 物理坐标（考虑缩放和偏移）"""
        return (
           #x * self.transform_matrix[0] + self.transform_matrix[4],
           #y * self.transform_matrix[3] + self.transform_matrix[5]
            x * self.scale_factor_abs + self.offset_x,
            y * self.scale_factor_abs + self.offset_y
        )

    def physical_to_logical(self, x, y):
        """物理坐标 → 逻辑坐标（逆向转换）"""
        return (
           # (x - self.transform_matrix[4]) / self.transform_matrix[0],
           # (y - self.transform_matrix[5]) / self.transform_matrix[3]
            (x - self.offset_x) / self.scale_factor_abs,
            (y - self.offset_y) / self.scale_factor_abs
        )

    def _on_zoom(self, event):
        """处理缩放事件"""
        # 获取当前鼠标位置的逻辑坐标
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        # 计算缩放因子
        self.scale_factor_rel = 1.1 if event.delta > 0 else 0.9
        self.scale_factor_abs *= self.scale_factor_rel
        self._zoom(x,y)
        self.callback_on_zoom_changed()
        # 应用缩放变换

    def zoom_abs(self, factor):
        xc,yc = self._get_viewport_center()
        self.scale_factor_rel = factor / self.scale_factor_abs
        self.scale_factor_abs = factor

        self._zoom(xc, yc)

    def _zoom(self, xc, yc):

        self.scale("all", xc, yc, self.scale_factor_rel, self.scale_factor_rel)

        # 更新变换矩阵
       # self.transform_matrix[0] *= _factor
       # self.transform_matrix[3] *= _factor
       # self.transform_matrix[4] = x - (x - self.transform_matrix[4]) * _factor
       # self.transform_matrix[5] = y - (y - self.transform_matrix[5]) * _factor

        self.offset_x = xc - (xc - self.offset_x) * self.scale_factor_rel
        self.offset_y = yc - (yc - self.offset_y) * self.scale_factor_rel

       #self.scale("all", x, y, factor, factor)
       #self.scale_factor *= factor

       ## 更新变换矩阵
       #self.transform_matrix[0] *= factor
       #self.transform_matrix[3] *= factor
       #self.transform_matrix[4] = x - (x - self.transform_matrix[4]) * factor
       #self.transform_matrix[5] = y - (y - self.transform_matrix[5]) * factor

        # 更新滚动区域
        self.update_scroll_region()

        # 保持视口中心
        #self._center_view(x, y, factor)
        self._update_text_font_sizes()

    def _center_view(self, center_x, center_y, factor):
        """保持缩放中心稳定"""
        # 计算视口尺寸
        view_width = self.winfo_width()
        view_height = self.winfo_height()

        # 计算新的滚动位置
        bbox = self.bbox("all")
        #h_scale = (bbox[2] - bbox[0]) / view_width
        #v_scale = (bbox[3] - bbox[1]) / view_height

        self.xview_moveto((center_x * factor - view_width / 2) / (bbox[2] - bbox[0]))
        self.yview_moveto((center_y * factor - view_height / 2) / (bbox[3] - bbox[1]))

    def _get_viewport_center(self):
        """獲取當前可見區域的中心座標（Canvas 坐標系）"""
        # 將屏幕坐標轉換為 Canvas 內部坐標
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()
        x0 = self.canvasx(0)
        y0 = self.canvasy(0)
        x1 = self.canvasx(screen_width)
        y1 = self.canvasy(screen_height)
        return (x0 + x1) / 2, (y0 + y1) / 2

    def on_pan_start(self, event):
        """記錄平移起始位置並設置掃描基準點"""
        #self.pan_start_x = event.x
        #self.pan_start_y = event.y

        # 關鍵步驟：設置掃描基準點
        self.scan_mark(event.x, event.y)

    def on_pan(self, event):
        """執行平移操作"""
        # 計算移動距離（用於界面顯示）
        #dx = event.x - self.pan_start_x
        #dy = event.y - self.pan_start_y

        # 核心平移方法
        self.scan_dragto(event.x, event.y, gain=1)

        # 更新起始點位置
        #self.pan_start_x = event.x
        #self.pan_start_y = event.y

        # 可選：顯示移動信息
        #print(f"平移距離: dx={dx}, dy={dy}")

    def find_closest(
        self, x, y, halo = None, start = None
    ):
        _x, _y = self.logical_to_physical(x, y)
        _halo = halo
        if _halo<0:
            _halo = 0
        return super().find_closest(_x, _y, halo=_halo, start=start)

    # 重写原生方法以支持逻辑坐标
    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        """创建矩形（使用逻辑坐标）"""
        _x1, _y1 = self.logical_to_physical(x1, y1)
        _x2, _y2 = self.logical_to_physical(x2, y2)
        return super().create_rectangle(
            _x1, _y1, _x2, _y2,
            #tags=kwargs.get("tags", ()) + ("logical",),
            **kwargs
        )

    def create_oval(self, x1, y1, x2, y2, **kwargs):
        """创建矩形（使用逻辑坐标）"""
        _x1, _y1 = self.logical_to_physical(x1, y1)
        _x2, _y2 = self.logical_to_physical(x2, y2)
        return super().create_oval(
            _x1, _y1, _x2, _y2,
            #tags=kwargs.get("tags", ()) + ("logical",),
            **kwargs
        )

    def create_line(self, *args, **kwargs):
        """
        创建线条（自动转换逻辑坐标）

        参数格式：
        - 坐标：x1,y1,x2,y2,... 或 [x1,y1,x2,y2,...]
        - 选项：必须使用关键字参数（如 smooth=True）
        """
        # 分离坐标参数和其他参数
        coord_args = []
        other_args = []

        # 处理坐标参数
        for arg in args:
            if isinstance(arg, (list, tuple)):
                coord_args.extend(arg)
            elif isinstance(arg, (int, float)):
                coord_args.append(arg)
            else:
                other_args.append(arg)

        # 检查坐标有效性
        if len(coord_args) % 2 != 0:
            raise ValueError("坐标参数必须成对出现（x,y）")
        if len(coord_args) < 2:
            raise ValueError("至少需要两个坐标点（起点和终点）")

        # 转换逻辑坐标 → 物理坐标
        physical_coords = []
        for i in range(0, len(coord_args), 2):
            x = coord_args[i]
            y = coord_args[i + 1]
            px, py = self.logical_to_physical(x, y)
            physical_coords.extend([px, py])

        # 合并参数
        new_args = tuple(physical_coords) + tuple(other_args)

        # 调用父类方法
        return super().create_line(*new_args, **kwargs)

    def create_text(self, x, y, text=None, **kwargs):
        """创建文本时记录原始字体属性"""
        # ... [原有坐标转换逻辑] ...
        if text is None:
            raise ValueError("text parameter must be provided")

        px, py = self.logical_to_physical(x, y)

        # 解析原始字体配置（无论用户传入的是字符串还是 Font 对象）
        font_spec = kwargs.get('font', 'TkDefaultFont')
        font_info = self._parse_font(font_spec)
        scaled_size = max(1, int(font_info['size'] * self.scale_factor_abs))
        # 生成唯一标签保存原始字体属性
        family_tag = f"font_family_{font_info['family'].replace(' ', '_')}"
        #size_tag = f"orig_size_{font_info['size']}"
        size_tag = f"orig_size_{scaled_size}"

        tags = list(kwargs.get("tags", ())) + [family_tag, size_tag, "logical_text"]
        kwargs['tags'] = tags
        # 创建物理字体对象并记录映射
        font_obj = tkFont.Font(
            family=font_info['family'],
            #size=font_info['size'],
            size=scaled_size,
            weight=font_info['weight'],
            slant=font_info['slant']
        )

        # 将字体对象与原始配置关联
        self.font_cache[str(font_obj)] = font_info  # 关键映射
        kwargs['font'] = font_obj

        return super().create_text(px, py, text=text,  **kwargs)

    def _parse_font(self, font_spec):
        """解析字体配置（支持 Font 对象/字符串/内部标识符）"""
        if isinstance(font_spec, tkFont.Font):
            # 直接获取字体属性
            return {
                'family': font_spec.actual()['family'],
                'size': font_spec.actual()['size'],
                'weight': font_spec.actual()['weight'],
                'slant': font_spec.actual()['slant']
            }
        elif isinstance(font_spec, str):
            if font_spec.startswith("font") and font_spec[4:].isdigit():
                # 如果是内部标识符（如 "font3"），从缓存获取原始配置
                return self.font_cache.get(font_spec, self._default_font_info())
            else:
                # 解析字符串格式（支持含空格的字体名）
                return self._parse_font_str(font_spec)
        return self._default_font_info()

    def _update_text_font_sizes(self):
        """基于原始属性更新字体"""
        #current_scale = round(self.scale_factor_abs, 2)
        current_scale = self.scale_factor_abs

        for item in self.find_withtag("logical_text"):
            # 获取字体标识符（可能是 "font3" 格式）
            font_spec = self.itemcget(item, "font")

            # 从缓存获取原始属性
            font_info = self._parse_font(font_spec)

            # 计算缩放后字号
            orig_size = self._get_orig_size_from_tags(item)  # 从标签获取原始字号
            scaled_size = max(1, int(orig_size * current_scale))

            # 创建新字体
            new_font = tkFont.Font(
                family=font_info['family'],
                size=scaled_size,
                weight=font_info['weight'],
                slant=font_info['slant']
            )

            # 更新显示字体并保留映射
            self.itemconfig(item, font=new_font)
            self.font_cache[str(new_font)] = font_info  # 保持映射关系

    def _default_font_info(self):
        """返回系统默认字体的属性字典"""
        # 获取 Tkinter 默认字体
        default_font = tkFont.nametofont("TkDefaultFont")

        return {
            'family': default_font.actual()['family'],
            'size': default_font.actual()['size'],
            'weight': default_font.actual()['weight'],
            'slant': default_font.actual()['slant']
        }

    def _get_orig_size_from_tags(self, item):
        """从标签中提取原始字号"""
        tags = self.gettags(item)
        for tag in tags:
            if tag.startswith("orig_size_"):
                return int(tag.split("_")[-1])
        return 10  # 默认值

    def _parse_font_str(self, font_str):
        """解析含空格字体名的字符串（如 'Times New Roman 12 bold'）"""
        # 使用正则表达式精确解析
        import re
        pattern = r"""
            ^
            (?P<family>.+?(?=\s+\d+|\s+(bold|italic)|$))  # 捕获至字号或样式前
            (?:\s+(?P<size>\d+))?                          # 字号
            (?:\s+(?P<styles>.*))?                         # 样式部分
            $
        """
        match = re.match(pattern, font_str.strip(), re.VERBOSE | re.IGNORECASE)

        if not match:
            return self._default_font_info()

        groups = match.groupdict()
        family = groups['family'].strip()
        size = int(groups['size']) if groups['size'] else 10
        styles = groups['styles'].lower().split() if groups['styles'] else []

        return {
            'family': family,
            'size': size,
            'weight': 'bold' if 'bold' in styles else 'normal',
            'slant': 'italic' if 'italic' in styles else 'roman'
        }

    def print(self):
        # 创建临时图像文件
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmpfile:
            image_path = self.save_canvas_as_image(tmpfile.name)
            self.print_image(image_path)

    def save_canvas_as_image(self, filename):
        """手动渲染 Canvas 内容到图像（增强版）"""
        # 获取 Canvas 尺寸
        #if hasattr(self, 'scrollregion') and self.scrollregion:
        #    width = self.scrollregion[2] - self.scrollregion[0]
        #    height = self.scrollregion[3] - self.scrollregion[1]
        #else:
        #    # 如果没有设置滚动区域，使用当前可见区域
        #    width = self.winfo_width()
        #    height = self.winfo_height()
        x1, y1, x2, y2 = self.bbox('all')
        width = max(x2 - x1, self.winfo_width())
        height = max( y2 - y1, self.winfo_height())
        margin = int( min(width, height, 600) / 60)
        # 确保有效尺寸
        if width < 10 or height < 10:
            width, height = 800, 600

        # 创建空白图像
        img = Image.new("RGBA", (width+2*margin, height+2*margin), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # 遍历 Canvas 所有项目并渲染
        for item in self.find_all():
            self.render_item(draw, item, x1-margin, y1-margin, width, height)

        # 保存图像
        if filename.lower().endswith('.jpg'):
            img = img.convert('RGB')
        img.save(filename)
        img.close()
        return filename

    def render_item(self, draw, item, canvas_origin_x, canvas_origin_y, canvas_width, canvas_height):
        """渲染单个 Canvas 项目（处理系统颜色）"""
        item_type = self.type(item)
        coords = self.coords(item)
        for i in range(0, int(len(coords)/2)):
            if canvas_origin_x <0:
                coords[2*i] -= canvas_origin_x
            if canvas_origin_y <0:
                coords[2*i+1] -= canvas_origin_y


        width = 1
        width_str = self.itemcget(item, "width")
        if width_str:
            try:
                width = int(width_str) if width_str else 1
            except ValueError:
                width = 1

        try:
            if item_type == "line":
                if len(coords) >= 4:
                    # 渲染线条
                    draw.line(coords,
                              fill=self.get_color( item, "fill"),
                              width=width)
                    # 如果设置了箭头，添加箭头
                    arrow = self.itemcget(item, "arrow")
                    arrow_shape = self.itemcget(item, "arrowshape")
                    if arrow != "none":
                        # 解析箭头形状
                        if arrow_shape:
                            try:
                                arrow_parts = [int(x) for x in arrow_shape.split()]
                                if len(arrow_parts) >= 3:
                                    a, b, c = arrow_parts[:3]
                                else:
                                    a, b, c = 8, 10, 3
                            except:
                                a, b, c = 8, 10, 3
                        else:
                            a, b, c = 8, 10, 3

                        # 计算箭头方向
                        x1, y1 = coords[:2]
                        x2, y2 = coords[-2:]
                        dx, dy = x2 - x1, y2 - y1
                        length = (dx ** 2 + dy ** 2) ** 0.5

                        if length > 0:
                            # 箭头方向单位向量
                            ux, uy = dx / length/2, dy / length/2

                            # 箭头尖端位置
                            tip_x, tip_y = x2, y2

                            # 如果箭头在起点
                            if arrow in ("first", "both"):
                                # 箭头尖端位置调整为起点
                                tip_x, tip_y = x1, y1
                                ux, uy = -ux, -uy

                            # 计算箭头两侧点
                            perp_x, perp_y = -uy * b, ux * b
                            back_x, back_y = -ux * a, -uy * a

                            # 箭头点
                            arrow_points = [
                                (tip_x, tip_y),
                                (tip_x + perp_x + back_x, tip_y + perp_y + back_y),
                                (tip_x - perp_x + back_x, tip_y - perp_y + back_y),
                                (tip_x, tip_y)
                            ]

                            # 绘制箭头
                            draw.polygon(arrow_points, fill=self.get_color(item, "fill"))

                            # 如果两端都有箭头
                            if arrow == "both":
                                # 另一端箭头
                                tip_x, tip_y = x2, y2
                                arrow_points = [
                                    (tip_x, tip_y),
                                    (tip_x + perp_x + back_x, tip_y + perp_y + back_y),
                                    (tip_x - perp_x + back_x, tip_y - perp_y + back_y),
                                    (tip_x, tip_y)
                                ]
                                draw.polygon(arrow_points, fill=self.get_color(item, "fill"))
            elif item_type == "rectangle":
                if len(coords) >= 4:
                    # 渲染矩形
                    draw.rectangle(coords,
                                   outline=self.get_color( item, "outline"),
                                   fill=self.get_color( item, "fill"),
                                   width= width)

            elif item_type == "oval":
                if len(coords) >= 4:
                    # 渲染椭圆
                    draw.ellipse(coords,
                                 outline=self.get_color( item, "outline"),
                                 fill=self.get_color( item, "fill"),
                                 width= width)

            elif item_type == "polygon":
                if len(coords) >= 6:  # 至少三个点 (x1,y1,x2,y2,x3,y3)
                    # 渲染多边形
                    draw.polygon(coords,
                                 outline=self.get_color(item, "outline"),
                                 fill=self.get_color( item, "fill"),
                                 width= width)

            elif item_type == "text":
                if coords:
                    # 渲染文本
                    text = self.itemcget(item, "text")
                    x, y = coords[:2]
                    fill_color = self.get_color( item, "fill")

                    # 获取字体
                    font = self.get_font( item)

                    # 确保文本在画布范围内
                    if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
                        draw.text((x-font.size*len(text)/4, y-font.size), text, fill=fill_color, font=font)

            # 添加其他项目类型处理（arc, bitmap, image等）

        except Exception as e:
            print(f"渲染项目 {item} ({item_type}) 时出错: {str(e)}")

    def get_color(self, item, attr):
        """安全获取颜色值，处理系统颜色名称"""
        try:
            color_str = self.itemcget(item, attr)

            # 处理空值或透明
            if not color_str or color_str.lower() in ["", "none", "transparent"]:
                return None

            # 处理系统颜色名称
            if color_str.startswith("system") or color_str in [
                "activebackground", "activeforeground",
                "background", "disabledforeground",
                "highlightbackground", "highlightcolor",
                "selectbackground", "selectforeground"
            ]:
                # 转换为实际颜色值
                rgb = self.winfo_rgb(color_str)
                return (rgb[0] // 256, rgb[1] // 256, rgb[2] // 256)

            # 尝试使用 tkinter 的颜色转换
            rgb = self.winfo_rgb(color_str)
            return (rgb[0] // 256, rgb[1] // 256, rgb[2] // 256)

        except:
            # 默认返回黑色
            return (0, 0, 0)

    def get_font(self, item):
        """安全获取字体对象"""
        try:
            font_str = self.itemcget(item, "font")
            if not font_str:
                return None

            # 尝试解析字体字符串（格式示例："Arial 12 bold"）
            font_parts = font_str.split()
            font_name = "Arial"
            font_size = 12
            font_style = "normal"

            # 查找尺寸部分
            for part in font_parts:
                if part.isdigit():
                    font_size = int(part)
                elif part in ["bold", "italic", "underline"]:
                    font_style = part

            # 尝试加载字体
            try:
                if font_style == "bold":
                    return ImageFont.truetype(font_name, font_size, index=1)  # bold
                elif font_style == "italic":
                    return ImageFont.truetype(font_name, font_size, index=2)  # italic
                else:
                    return ImageFont.truetype(font_name, font_size)
            except:
                return ImageFont.load_default()

        except:
            return ImageFont.load_default()

    def print_image(self, filename: str):
        # 确保文件完全写入磁盘
        self.update()  # 刷新UI
        time.sleep(0.5)  # 等待文件写入

        """打印图像文件"""
        try:
            # Windows
            os.startfile(filename, "print")
        except :
            # macOS
            try:
                subprocess.run(["lp", filename])
            except:
                # Linux
                try:
                    subprocess.run(["lpr", filename])
                except:
                    print("无法自动打印，请手动打印文件:", filename)


   ## 添加其他图形方法的类似重写...
class PROJECT_PAGE():
    def __init__(self, parent: TK_WINDOW,
                 callback_on_node_clicked:Callable,
                 callback_on_changed:Callable,
                 callback_on_zoom_changed:Callable,
                 callback_on_node_deleted:Callable,
                 name: Optional[str] = None, project : Optional[WORKFLOW_PROJECT] = None):
        self.parent = parent

        self.index_tab = 0
        self.callback_on_node_clicked = callback_on_node_clicked
        self.callback_on_node_deleted = callback_on_node_deleted
        self.callback_on_changed = callback_on_changed
        self.callback_on_zoom_changed=callback_on_zoom_changed
        #self.is_changed =  False

        self.current_node_key  = ""
        self.current_workflow_iteration_key = ""
        self.enum_node_to_insert = None
        #self.new_node_picked = None
        self.last_canvas_click = None
        self.current_knot_connector : Optional[KNOT_CONNECTOR] = None
        self.enum_canvas_operation : Optional[ENUM_CANVAS_OPERATION] = None

        #self.scale_factor = 1.0
        parent.grid_rowconfigure(0, weight=1)  # 第 0 行可擴展
        parent.grid_columnconfigure(0, weight=1)
        self.canvas = CanvasScrollZoom(parent, bg='white')
        self.canvas.set_callback(self.callback_on_zoom_changed)
        #self.canvas = tk.Canvas(parent, bg='white')
        #self.scroll_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.canvas.xview)
        #self.scroll_y = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        #self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')


        self.canvas.bind("<Button-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Delete>", self.on_canvas_delete)
        self.canvas.bind("<Motion>", self.on_canvas_hover)  # 鼠标进入时触发
        self.canvas.bind("<Leave>", self.on_canvas_hover_end)  # 鼠标离开时触发
        self.canvas.bind("<Control-Button-1>", self.on_canvas_ctrl_press)

        if project:
            self.project = project
        else:
            self.project =WORKFLOW_PROJECT( name=name )
            self.init_graphic_workflow(self.project.workflow)


        self.project.set_update_graphic(self.draw_current_node_box)

        self.current_workflow_iteration_key = self.project.workflow.key
        self.edit_tab_text = None
        self.phantom_node_graphic : Optional[NODE_GRAPHIC] = None

        self.is_press = False
        self.is_ctrl_press = False
        #self.is_hover=True
        self.is_hover=False
        self.is_drag = False
        self.enum_run_type: ENUM_RUN_TYPE = ENUM_RUN_TYPE.STOP
        self.redraw_canvas()
        self.update_current_workflow_parent_graphic()
       # parent.update_idletasks()  # 强制完成所有布局计算
       # self._update_button_position()  # 手动触发首次定位

    ## 在以下位置调用：
    ## 1. _add_floating_zoom_buttons 末尾
    ## 2. zoom 方法末尾
    ## 3. _update_button_position 末尾
    def zoom(self, factor):
        self.canvas.zoom_abs(factor)


    def set_project(self, project: WORKFLOW_PROJECT):
        self.project = project

    def set_index_tab(self, index_tab:int):
        self.index_tab = index_tab

    def on_current_node_changed(self, node_key: str):
        self.current_node_key = node_key
        self.callback_on_node_clicked()

    def reset_current_node_key(self):
        # self.current_node_key = self.start_node_key
        self.current_node_key = ""
        self.enum_run_type = ENUM_RUN_TYPE.STOP

    def set_graphic_label_text(self, id_label: int,  new_text:str):
        self.canvas.itemconfig(id_label, text=new_text)

    def get_current_node_graphic(self):
        return self.get_node_graphic(self.current_node_key)

    def get_node_graphic(self, key:str):
        return self.project.controller_node_graphic.get_node_graphic_by_key(key)

    def insert_node_graphic(self, node_graphic: NODE_GRAPHIC):
        node_graphic.graphic.x = self.last_canvas_click[0]
        node_graphic.graphic.y = self.last_canvas_click[1]
        node_graphic.set_node_key( self.project.controller_node_graphic.get_new_node_key(node_graphic.key))
        node_graphic.graphic.refresh_knots_center()
        self.project.controller_node_graphic.add_node_graphic(node_graphic)

        if node_graphic.node.enum_node == ENUM_NODE.NODE_ITERATION:
            self.init_graphic_workflow(cast(NODE_ITERATION, node_graphic.node).workflow)
        self.update_parent_node_graphic(node_graphic)
        self.draw_graphic(node_graphic, True)

        self.project.is_changed = True
        self.callback_on_changed()


    def add_new_node(self, parent_key:Optional[str]=None) -> NODE_GRAPHIC:

        new_node : WORK_NODE = self.project.controller_node_graphic.add_new_node(enum_node=self.enum_node_to_insert,
                                                                                 parent_key= parent_key or self.current_workflow_iteration_key,
                                                                                # mount_manager=self.project.mount_manager,
                                                                                 )
        new_node.set_global_variables(self.project.global_variables)

        if new_node.enum_node in LIST_NEED_LLMS_API:
            new_node.set_llms_api(self.project.llms_api)

        #self.enum_node_to_insert = None
        is_redraw = False
      
        new_graphic = WORKNODE_GRAPHIC(  node_key=new_node.key, x = self.last_canvas_click[0], y=self.last_canvas_click[1])

        new_node_graphic = NODE_GRAPHIC(new_node, new_graphic)

        self.project.controller_node_graphic.update_graphic(new_graphic)
        if new_node.enum_node == ENUM_NODE.NODE_ITERATION:
            self.init_graphic_workflow( cast(NODE_ITERATION,new_node).workflow)
        self.update_parent_node_graphic(new_node_graphic)
        if is_redraw:
            self.redraw_canvas()
        else:
            self.draw_graphic(new_node_graphic, True)

        self.project.is_changed = True
        self.callback_on_changed()
        return new_node_graphic



    def init_graphic_workflow(self, workflow: WORKFLOW):
        node_key_start = workflow.start_node_key
        node_key_end = self.project.controller_node_graphic.get_node_by_key(node_key_start).get_next_node_key()
       # level=0
        if workflow.parent_key and len(workflow.parent_key)>0:
            parent_node_graphic = self.project.controller_node_graphic.get_node_graphic_by_key(workflow.parent_key)
            #level = parent_node_graphic.graphic.get_level()+1
            start_x = parent_node_graphic.graphic.x - NODE_WIDTH * 1.5
            start_y = parent_node_graphic.graphic.y
            end_x = parent_node_graphic.graphic.x + NODE_WIDTH * 1.5
            end_y = start_y
        else:
            parent_width = self.canvas.winfo_screenwidth()
            parent_height = self.canvas.winfo_screenheight()
            start_x = parent_width / 4 - NODE_WIDTH * 1.5
            start_y = parent_height / 4
            end_x = parent_width / 4 + NODE_WIDTH* 1.5
            end_y = start_y

        graphic_start = WORKNODE_GRAPHIC(node_key=node_key_start, x=start_x,       y=start_y,)
        graphic_end = WORKNODE_GRAPHIC(node_key=node_key_end, x=end_x,y= end_y ,     )
        graphic_start.list_output_knot[0].line_to_x=graphic_end.input_knot.line_to_x
        graphic_start.list_output_knot[0].line_to_y = graphic_end.input_knot.line_to_y
       #graphic_start.list_output_knot[0].node_key_start = node_key_start
        graphic_start.list_output_knot[0].node_key_to = node_key_end

        self.project.controller_node_graphic.update_graphic(graphic_start)
        self.project.controller_node_graphic.update_graphic(graphic_end)

       # self.update_current_workflow_parent_graphic()
       # self.update_workflow_parent_graphic(workflow)

    def get_current_workflow(self)->WORKFLOW:
        if self.current_workflow_iteration_key == self.project.workflow.key:
            workflow = self.project.workflow
        else:
            workflow = cast(NODE_ITERATION, self.project.controller_node_graphic.get_node_by_key(
                self.current_workflow_iteration_key)).workflow
        return workflow



    def update_current_workflow_parent_graphic(self):
        if is_string_valid(self.current_workflow_iteration_key):
            workflow = self.get_current_workflow()
            self.update_parent_workflow_graphic(workflow)

            #self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_parent_node_graphic(self, node_graphic: NODE_GRAPHIC):
        node = node_graphic.node
        if node.enum_node == ENUM_NODE.NODE_ITERATION:
            self.update_parent_workflow_graphic(cast(NODE_ITERATION, node).workflow)

            if node.parent_key == self.project.workflow.key:
                parent_workflow = self.project.workflow
            else:
                parent_node_iteration = self.project.controller_node_graphic.get_node_by_key(node.parent_key)
                parent_workflow = cast(NODE_ITERATION, parent_node_iteration).workflow
        else:
            parent_workflow = self.get_current_workflow()
        self.update_parent_workflow_graphic(parent_workflow)

    def update_parent_workflow_graphic(self, workflow: WORKFLOW):

        graphic_range_workflow = self.get_graphic_range_workflow(workflow)

        if is_string_valid(workflow.parent_key):
            parent_node_graphic : NODE_GRAPHIC = self.project.controller_node_graphic.get_node_graphic_by_key(workflow.parent_key)
          #  parent_graphic_range = parent_node_graphic.graphic.combine_range(graphic_range_workflow)

          # parent_node_graphic.graphic.width = parent_graphic_range[2] - parent_graphic_range[0] + NODE_WIDTH*2
          # parent_node_graphic.graphic.height = parent_graphic_range[3] - parent_graphic_range[1] + NODE_HEIGHT*2
          # x = (parent_graphic_range[0] + parent_graphic_range[2])/2
          # y = (parent_graphic_range[1] + parent_graphic_range[3]) / 2

            parent_node_graphic.graphic.width = graphic_range_workflow[2] - graphic_range_workflow[0] + NODE_WIDTH
            parent_node_graphic.graphic.height = graphic_range_workflow[3] - graphic_range_workflow[1] + NODE_HEIGHT * 2
            x = (graphic_range_workflow[0] + graphic_range_workflow[2]) / 2
            y = (graphic_range_workflow[1] + graphic_range_workflow[3]) / 2
            parent_node_graphic.graphic.set_knots_center(x, y)
            self.project.controller_node_graphic.update_graphic(parent_node_graphic.graphic)

            if is_string_valid(parent_node_graphic.node.parent_key):
                grand_parent_workflow=None
                if parent_node_graphic.node.parent_key == self.project.workflow.key:
                    grand_parent_workflow = self.project.workflow
                else:
                    grand_parent_node_graphic: NODE_GRAPHIC = self.project.controller_node_graphic.get_node_graphic_by_key(
                        parent_node_graphic.node.parent_key)
                    if grand_parent_node_graphic.node.enum_node == ENUM_NODE.NODE_ITERATION:
                        grand_parent_workflow= cast(NODE_ITERATION, grand_parent_node_graphic.node).workflow
                if grand_parent_workflow:
                    self.update_parent_workflow_graphic(grand_parent_workflow)

        else:
            screen_width = self.canvas.winfo_screenwidth()
            screen_height = self.canvas.winfo_screenheight()
            if graphic_range_workflow[2] > self.canvas.winfo_screenwidth():
                self.canvas.configure(width=graphic_range_workflow[2])
            if graphic_range_workflow[3] > self.canvas.winfo_screenheight():
                self.canvas.configure(height=graphic_range_workflow[3])


        self.canvas.update_idletasks()  # 确保内容已渲染
        self.canvas.update_scroll_region()

    def get_graphic_range_workflow(self, workflow: WORKFLOW) -> Tuple[float, float, float, float]:
        node_key = workflow.start_node_key

        is_first = True
        workflow_range = None
        parent_key = workflow.parent_key if workflow.parent_key else workflow.key
        for node_graphic in self.project.controller_node_graphic.dict_node_graphic.values():
            if node_graphic.node.parent_key == parent_key:
                if is_first:
                    is_first = False
                    workflow_range = node_graphic.graphic.get_graphic_range()
                else:
                    workflow_range = node_graphic.graphic.combine_range(workflow_range)
        return workflow_range

    def change_current_node_key(self,  new_current_node_key):
        current_node_graphic = self.get_current_node_graphic()
        self.current_node_key = new_current_node_key
        if not current_node_graphic:
            current_node_graphic = self.get_current_node_graphic()
        self.clear_graphic(current_node_graphic)
        #self.project.controller_node_graphic.change_name(self.current_node_key, new_current_node_key)
        current_node_graphic = self.get_current_node_graphic()
        self.draw_graphic(current_node_graphic, True)
        self.project.is_changed=True
        self.callback_on_changed()

    def update_current_node(self, node_modified: WORK_NODE):
        current_node_graphic = self.get_current_node_graphic()

        if current_node_graphic.key != node_modified.key:
            list_tuple_prev = self.project.controller_node_graphic.get_node_key_by_node_key_next(self.current_node_key)

            if len(list_tuple_prev) > 0:
                for tuple_prev in list_tuple_prev:
                    node_key_prev = tuple_prev[0]
                    i = tuple_prev[1]
                    node_graphic_prev = self.get_node_graphic(node_key_prev)
                    if node_graphic_prev:
                        node_graphic_prev.set_next_node_key(i, node_modified.key)
                        self.project.controller_node_graphic.update_node_graphic(node_graphic_prev)

                    self.project.controller_node_graphic.delete_node_graphic_by_key(
                        self.current_node_key)

        self.current_node_key = node_modified.key
        current_node_graphic = self.get_current_node_graphic()
        current_node_graphic.node = node_modified

        if node_modified.enum_node == ENUM_NODE.NODE_BRANCH:
            node_branch : NODE_BRANCH = cast(NODE_BRANCH, node_modified)
            current_node_graphic.node.set_next_nodes_number(node_branch.number_of_branches)
            current_node_graphic.graphic.set_output_knot_number(node_branch.number_of_branches)

        if node_modified.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
            node_categorized_by_llm: NODE_CATEGORIZED_BY_LLM = cast(NODE_CATEGORIZED_BY_LLM, node_modified)
            knot_number = node_categorized_by_llm.get_next_nodes_number()
          #  current_node_graphic.node.set_next_nodes_number(knot_number)
          #  current_node_graphic.graphic.set_output_knot_number(knot_number)

        self.project.controller_node_graphic.update_node_graphic(current_node_graphic)
        self.draw_graphic(current_node_graphic, is_draw_children=True)
        self.draw_node_connection(current_node_graphic)

        list_tuple_prev = self.project.controller_node_graphic.get_node_key_by_node_key_next(self.current_node_key)
        if len(list_tuple_prev) > 0:
            for tuple_prev in list_tuple_prev:
                node_key_prev = tuple_prev[0]
                node_graphic_prev = self.get_node_graphic(node_key_prev)
                if node_graphic_prev:
                    self.draw_node_connection(node_graphic_prev)
        self.project.is_changed = True
        self.callback_on_changed()

    def update_node_graphic(self, node_graphic: NODE_GRAPHIC):
        self.project.controller_node_graphic.update_node_graphic(node_graphic)

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_graphic(self, node_graphic: NODE_GRAPHIC):
        graphic: WORKNODE_GRAPHIC = node_graphic.graphic

        if graphic.id_body:
            self.canvas.delete(graphic.id_body)

        if graphic.id_label:
            self.canvas.delete(graphic.id_label)

        if graphic.input_knot and graphic.input_knot.id_knot:
            self.canvas.delete(graphic.input_knot.id_knot)

        len_list_output_knot = len(graphic.list_output_knot)

        if len_list_output_knot>0:
            #if node_graphic.node.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
            #    node = cast(NODE_CATEGORIZED_BY_LLM, node_graphic.node)
            #    if node.is_branch:
            #        len_list_output_knot = 1
#
            for i in range(0, len_list_output_knot):
                output_knot_connector =  graphic.list_output_knot[i]
                if output_knot_connector.id_knot:
                    self.canvas.delete(output_knot_connector.id_knot)
                if output_knot_connector.id_line:
                    self.canvas.delete(output_knot_connector.id_line)


    def redraw_canvas(self):
        self.clear_canvas()
        # 绘制所有节点
        self.draw_workflow_graphic(self.project.workflow, True)
        #self.update_workflow_parent_graphic(self.project.workflow)
        # 绘制连接线
       # self.add_all_connections()
        self.canvas.update_scroll_region()

    def draw_workflow_graphic(self, workflow: WORKFLOW, is_draw_children: Optional[bool] = False):
        parent_key = workflow.parent_key if workflow.parent_key else workflow.key
        for node_graphic in self.project.controller_node_graphic.dict_node_graphic.values():
            if node_graphic.node.parent_key == parent_key:
                self.draw_graphic(node_graphic, is_draw_children)
                self.draw_node_connection(node_graphic)
        #self.draw_workflow_connections(workflow)

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        # 圓角半徑 radius
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        # 使用 smooth=True 讓轉折處變圓滑
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def draw_graphic(self, node_graphic: NODE_GRAPHIC, is_draw_children: Optional[bool] = False, is_dash: Optional[bool] = False):
        # 节点绘制逻辑
        #_node_graphic = deepcopy(node_graphic)
        node : WORK_NODE = node_graphic.node
        #node_branch: NODE_BRANCH = node_graphic.node
        graphic : WORKNODE_GRAPHIC = node_graphic.graphic
        fill_color = graphic.fill_color

        if not is_dash and node.enum_node == ENUM_NODE.NODE_ITERATION:
            if is_even(cast(NODE_ITERATION, node).depth):
                fill_color=FILL_COLOR_ITERATION_EVEN
            else:
                fill_color=FILL_COLOR_ITERATION_ODD

        self.clear_graphic(node_graphic)

        knots_number = len(graphic.list_output_knot)
        if node.enum_node ==  ENUM_NODE.NODE_BRANCH:
           # node_branch: NODE_BRANCH = node
            knots_number = cast(NODE_BRANCH, node).number_of_branches

        if node.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
            knots_number = cast(NODE_CATEGORIZED_BY_LLM, node).get_next_nodes_number()

        if node.enum_node in (ENUM_NODE.NODE_BRANCH, ENUM_NODE.NODE_CATEGORIZED_BY_LLM):
            graphic.set_output_knot_number(knots_number)
            graphic.set_input_knot_center()

        x = graphic.x
        y = graphic.y
        w = graphic.width
        h = graphic.height
        m = knots_number
        radius =  max(20, min(4, int(min(w, h)/10)))

        outline_width = graphic.outline_width
        outline_color = graphic.outline_color
        if node.key == self.current_node_key:
            outline_width *= 2
            outline_color = "red"

        dash_style = DASH_STYLES['solid']
        if is_dash:
            dash_style= DASH_STYLES['dashed']
            outline_color = "grey"

        #graphic.id_body = self.canvas.create_rectangle(
        #    x-w/2, y-h/2, x + w/2, y + h/2,
        #    fill=fill_color, outline=outline_color, width=outline_width,
        #    dash=dash_style,
        #    tags=("node", graphic.node_key, node.enum_node.value)
        #)

        graphic.id_body = self.draw_rounded_rect(
            x-w/2, y-h/2, x + w/2, y + h/2,
            radius=radius,
            fill=fill_color,
            outline=outline_color,
            width=outline_width,
            dash=dash_style,
            tags=("node", graphic.node_key, node.enum_node.value)
        )
        #self.canvas.lift(graphic.id_body)
        graphic.id_label = self.canvas.create_text(
            x ,y if node.enum_node not in [ENUM_NODE.NODE_ITERATION, ENUM_NODE.NODE_BRANCH] else y-h/2+10,
            text= title(node.name),
            width = NODE_WIDTH,
            font=(graphic.label_font, graphic.label_font_size),
            tags=("label", graphic.node_key, node.enum_node.value)
        )

        dia = graphic.knot_diameter

        if not is_dash:
            if node.enum_node != ENUM_NODE.NODE_START:
                graphic.input_knot.id_knot = self.canvas.create_oval(
                    graphic.input_knot.knot_x - graphic.input_knot.knot_diameter/2, graphic.input_knot.knot_y - graphic.input_knot.knot_diameter/2,
                    graphic.input_knot.knot_x + graphic.input_knot.knot_diameter/2, graphic.input_knot.knot_y + graphic.input_knot.knot_diameter/2,
                    fill="#808080", outline="#404040",
                    tags = ("input_knot", graphic.node_key)
                )

            if node.enum_node != ENUM_NODE.NODE_END:
                for i in range(0, knots_number):
                    knot_connector = graphic.list_output_knot[i]
                    knot_connector.id_knot =  self.canvas.create_oval(
                        knot_connector.knot_x - knot_connector.knot_diameter / 2,
                        knot_connector.knot_y - knot_connector.knot_diameter / 2,
                        knot_connector.knot_x + knot_connector.knot_diameter / 2,
                        knot_connector.knot_y + knot_connector.knot_diameter / 2,
                        fill="#808080", outline="#404040",
                        tags=("output_knot", graphic.node_key, str(i))
                    )
                    graphic.list_output_knot[i]=knot_connector

            node_graphic.set_graphic(graphic=graphic)
            self.update_node_graphic(node_graphic)

            if node.enum_node == ENUM_NODE.NODE_ITERATION and is_draw_children:
                #node_iteration : NODE_ITERATION = node
                self.draw_workflow_graphic(cast(NODE_ITERATION, node).workflow, is_draw_children)

    def refresh(self):
        for node_graphic in self.project.controller_node_graphic.dict_node_graphic.values():
            if node_graphic.node.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
                self.draw_graphic(node_graphic)
                self.refresh_node_connection(node_graphic)


    def refresh_node(self, node_graphic: NODE_GRAPHIC):
        node : WORK_NODE = node_graphic.node
        graphic : WORKNODE_GRAPHIC = node_graphic.graphic

        knots_number = len(graphic.list_output_knot)
        if node.enum_node ==  ENUM_NODE.NODE_BRANCH:
           # node_branch: NODE_BRANCH = node
            knots_number = cast(NODE_BRANCH, node).number_of_branches

        if node.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
            knots_number = cast(NODE_CATEGORIZED_BY_LLM, node).get_next_nodes_number()

        if node.enum_node in (ENUM_NODE.NODE_BRANCH, ENUM_NODE.NODE_CATEGORIZED_BY_LLM):
            graphic.set_output_knot_number(knots_number)

        x = graphic.x
        y = graphic.y
        w = graphic.width
        h = graphic.height
        m = knots_number
        dia = graphic.knot_diameter

        self.canvas.coords(graphic.id_body, x-w/2, y-h/2, x + w/2, y + h/2)
        self.canvas.coords(graphic.id_label,x, y if node.enum_node not in [ENUM_NODE.NODE_ITERATION, ENUM_NODE.NODE_BRANCH] else y-h/2+10)

        if node.enum_node != ENUM_NODE.NODE_START:
            self.canvas.coords(graphic.input_knot.id_knot,
                               graphic.input_knot.knot_x - graphic.input_knot.knot_diameter / 2,
                               graphic.input_knot.knot_y - graphic.input_knot.knot_diameter / 2,
                               graphic.input_knot.knot_x + graphic.input_knot.knot_diameter / 2,
                               graphic.input_knot.knot_y + graphic.input_knot.knot_diameter / 2)

        if node.enum_node != ENUM_NODE.NODE_END:
            for i in range(0, knots_number):
                knot_connector = graphic.list_output_knot[i]

                self.canvas.coords(knot_connector.id_knot,
                                       knot_connector.knot_x - knot_connector.knot_diameter / 2,
                                       knot_connector.knot_y - knot_connector.knot_diameter / 2,
                                       knot_connector.knot_x + knot_connector.knot_diameter / 2,
                                       knot_connector.knot_y + knot_connector.knot_diameter / 2, )
                graphic.list_output_knot[i]=knot_connector

        node_graphic.set_graphic(graphic=graphic)
        self.update_node_graphic(node_graphic)

    def refresh_node_connection(self, node_graphic: NODE_GRAPHIC):
        graphic: WORKNODE_GRAPHIC = node_graphic.graphic
        is_modified = False
        input_knot = graphic.input_knot
        list_tuple_prev = self.project.controller_node_graphic.get_node_key_by_node_key_next(graphic.node_key)

        if list_tuple_prev and len(list_tuple_prev) > 0:
            for tuple_prev in list_tuple_prev:
                node_key_prev = tuple_prev[0]
                i = tuple_prev[1]
                node_graphic_prev=self.project.controller_node_graphic.get_node_graphic_by_key(node_key_prev)
                output_knot_connector = node_graphic_prev.graphic.list_output_knot[i]
                output_knot_connector.line_to_x = input_knot.line_to_x
                output_knot_connector.line_to_y = input_knot.line_to_y
                self.refresh_connection(output_knot_connector)
                node_graphic_prev.graphic.list_output_knot[i]=output_knot_connector
                self.project.controller_node_graphic.update_node_graphic(node_graphic_prev)

        if len(graphic.list_output_knot) > 0:
            for i in range(0, len(graphic.list_output_knot)):
               output_knot_connector = graphic.list_output_knot[i]

               if is_string_valid(output_knot_connector.node_key_to):
                   is_modified = True
                   self.refresh_connection(output_knot_connector)
                   graphic.list_output_knot[i] = output_knot_connector
            if is_modified:
               self.project.controller_node_graphic.update_graphic(graphic)

    def draw_workflow_connections(self, workflow: WORKFLOW):
       # 绘制所有节点之间的连接线
       parent_key = workflow.parent_key if workflow.parent_key else workflow.key
       for node_graphic in workflow.controller_node_graphic.dict_node_graphic.values():
           node = node_graphic.node
           if node.parent_key == parent_key:
                self.draw_node_connection(node_graphic)


    def draw_node_connection(self, node_graphic: NODE_GRAPHIC):
        node : WORK_NODE = node_graphic.node
        graphic: WORKNODE_GRAPHIC = node_graphic.graphic
        is_modified = False

        len_list_output_knot = len(graphic.list_output_knot)

        if len_list_output_knot > 0:
            if node.enum_node == ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
                node = cast(NODE_CATEGORIZED_BY_LLM, node)
                if not node.is_branch:
                    len_list_output_knot = 1

            for i in range(0, len_list_output_knot):
                output_knot_connector = graphic.list_output_knot[i]

                if is_string_valid(output_knot_connector.node_key_to):
                   is_modified = True
                   self.canvas.delete(output_knot_connector.id_line)
                   next_node_graphic = self.project.controller_node_graphic.get_node_graphic_by_key(
                       output_knot_connector.node_key_to)
                   if next_node_graphic:
                       input_knot = next_node_graphic.graphic.input_knot
                       output_knot_connector.line_to_x = input_knot.line_to_x
                       output_knot_connector.line_to_y = input_knot.line_to_y
                       output_knot_connector.id_line = self.draw_connection(output_knot_connector)
                       graphic.list_output_knot[i] = output_knot_connector
            if is_modified:
               node_graphic.graphic = graphic
               self.project.controller_node_graphic.update_node_graphic(node_graphic)

    def refresh_connection(self, knot_connector : KNOT_CONNECTOR):

        start_x = knot_connector.line_from_x
        start_y = knot_connector.line_from_y
        end_x = knot_connector.line_to_x
        end_y = knot_connector.line_to_y
        c1_x = start_x + (end_x-start_x)/3
        c1_y = start_y +(end_y - start_y)/4
        c2_x = start_x + (end_x - start_x) / 3 *2
        c2_y = start_y + (end_y - start_y) / 4 *3
        points = [
            start_x, start_y,
            c1_x, c1_y,
            c2_x, c2_y,
            end_x, end_y,
        ]
        #print(f"start({start_x}, {start_y}), end({end_x}, {end_y})")
        #self.canvas.coords(knot_connector.id_line, *points)
        self.canvas.coords(knot_connector.id_line,
                           start_x, start_y,
            c1_x, c1_y,
            c2_x, c2_y,
            end_x, end_y,)

    def draw_connection(self, knot_connector : KNOT_CONNECTOR, is_current=False)->int:

        start_x = knot_connector.line_from_x
        start_y = knot_connector.line_from_y
        end_x = knot_connector.line_to_x
        end_y = knot_connector.line_to_y
        dx = end_x - start_x
        dy = end_y - start_y

        graphic_from =  self.get_node_graphic(knot_connector.node_key_from).graphic
        graphic_to = None
        if is_string_valid(knot_connector.node_key_to):
            node_graphic = self.get_node_graphic(knot_connector.node_key_to)
            if node_graphic:
                graphic_to = node_graphic.graphic

        is_output_knot_right = graphic_from.is_output_knot_right
        is_input_knot_left = True
        if graphic_to:
            is_input_knot_left = graphic_to.is_input_knot_left

        m , n = 4, 6

        if is_output_knot_right:
            c1_x = start_x + dx/m
            c1_y = start_y +dy/n
        else:
            c1_x = start_x + dx / n
            c1_y = start_y + dy / m

        if is_input_knot_left:
            c2_x = start_x + dx / m * (m-1)
            c2_y = start_y + dy / n * (n-1)
        else:
            c2_x = start_x + dx / n * (n-1)
            c2_y = start_y + dy / m * (m-1)

        points = [
            start_x, start_y,
            c1_x, c1_y,
            c2_x, c2_y,
            end_x, end_y,
        ]
        #print(f"start({start_x}, {start_y}), end({end_x}, {end_y})")
        width = 1
        if is_current:
            width = 2
        id_line = self.canvas.create_line(
            points,
            smooth=True, splinesteps=20,
            arrow=tk.LAST,
            arrowshape=(8, 8, 3),  # 箭头形状 (长度,宽度,尖部长度)
            width=width, fill="blue", tags=("connector", knot_connector.node_key_from, str(knot_connector.index))
        )

        return id_line

    def move_node(self, node_graphic: NODE_GRAPHIC, dx, dy):
      #  node_graphic.graphic.move_center(dx, dy)
        graphic = node_graphic.graphic
        self.canvas.move(graphic.id_body, dx, dy)
        self.canvas.move(graphic.id_label, dx, dy)
        self.canvas.move(graphic.input_knot.id_knot, dx, dy)
        graphic.move_center(dx, dy)
        for i in range(0, graphic.output_knot_number):
           knot_connector =  graphic.list_output_knot[i]
           self.canvas.move(knot_connector.id_knot, dx, dy)
           self.canvas.move(knot_connector.id_line, dx, dy)
           graphic.list_output_knot[i] = knot_connector
        node_graphic.graphic = graphic
        self.project.controller_node_graphic.update_node_graphic(node_graphic)

        node = node_graphic.node
        if node.enum_node == ENUM_NODE.NODE_ITERATION:
            for node_graphic in self.project.controller_node_graphic.dict_node_graphic.values():
                if node_graphic.node.parent_key == node.key:
                    self.move_node(node_graphic, dx, dy)



    # 以下是事件处理函数 -------------------------------------------------


    def on_canvas_press(self, event):
        if self.is_press:
            return
        self.is_press=True
        self.is_drag = False
        #self.is_hover=False
        self.canvas.focus_set()
        x, y = self.canvas.get_event_coord(event)
        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        # 处理画布点击事件
        self.last_canvas_click = (x, y)
        #print(f"Press 邏輯座標: ({x}, {y})")

        start = None
        if self.phantom_node_graphic:
            start = self.phantom_node_graphic.graphic.id_body
        elif self.current_knot_connector:
            start = self.current_knot_connector.id_line

        pressed_object, item_tags = self.smart_get_items_at_location(x, y, start=start)

        is_possible_insert=True
        parent_key = None
        if pressed_object:
            is_possible_insert = False
            match pressed_object:
                case "node":
                    node_key = item_tags[1]
                    if is_string_valid(node_key):
                        node = self.project.controller_node_graphic.get_node_by_key(node_key)
                        if node:
                            if node.enum_node == ENUM_NODE.NODE_ITERATION and self.enum_canvas_operation and self.enum_canvas_operation == ENUM_CANVAS_OPERATION.ADD_NODE and self.enum_node_to_insert:
                                is_possible_insert=True
                                parent_key = node_key
                            else:
                                self.draw_current_node_box(node_key)
                                self.callback_on_node_clicked()
                                self.current_knot_connector = None
                                self.enum_canvas_operation = ENUM_CANVAS_OPERATION.DRAG_MOVE
                        #else:
                            #print(f"node_key={node_key}")
                case "output_knot":
                    self.handle_knot_press(item_tags)
                    self.enum_canvas_operation = ENUM_CANVAS_OPERATION.DRAG_CONNECT
                case  "connector":
                    self.handle_connector_press(item_tags)
                #case _:
                #    match pressed_object_nearby:
                #        case "connector":
                #            self.handle_connector_press(item_tags_nearby)

        elif not self.enum_canvas_operation :
            self.enum_canvas_operation = ENUM_CANVAS_OPERATION.PAN
            self.canvas.on_pan_start(event)
            #print(f"Pan On")

        if is_possible_insert:
            if self.enum_canvas_operation and self.enum_canvas_operation == ENUM_CANVAS_OPERATION.ADD_NODE and self.enum_node_to_insert:
                self.insert_node(parent_key)

                #self.callback_on_changed()
                #self.update_current_workflow_parent_graphic()

        #self.is_hover = True
        self.is_press = False

    def insert_node(self, parent_key: Optional[str] = None)->str:
        node_graphic: NODE_GRAPHIC =  self.add_new_node(parent_key)
        self.draw_current_node_box(node_graphic.key)
        if self.enum_node_to_insert == ENUM_NODE.NODE_ITERATION:
            self.redraw_canvas()
        self.enum_canvas_operation = None
        self.enum_node_to_insert = None
        if self.phantom_node_graphic:
            self.clear_graphic(self.phantom_node_graphic)
            self.phantom_node_graphic = None

        self.callback_on_node_clicked()
        return node_graphic.key

    def on_canvas_ctrl_press(self, event):
        if self.is_ctrl_press:
            return
        self.is_ctrl_press = True

        x, y = self.canvas.get_event_coord(event)
        self.last_canvas_click = (x, y)
        #print(f"Ctrl Press 邏輯座標: ({x}, {y})")

        pressed_object, item_tags = self.get_items_at_location(x, y)

        if pressed_object:
            match pressed_object:
                case "node":
                    node_key = item_tags[1]
                    if is_string_valid(node_key):
                        node_graphic = self.project.controller_node_graphic.get_node_graphic_by_key(node_key)
                        if node_graphic:
                            c_x = node_graphic.graphic.x
                            c_y = node_graphic.graphic.y
                            w = node_graphic.graphic.width
                            h = node_graphic.graphic.height

                            dx_l = abs(c_x-w/2-x)
                            dx_r = abs(c_x+w/2-x)
                            dy_t = abs(c_y - h / 2 - y)
                            dy_b = abs(c_y + h / 2 - y)

                            is_changed=False
                            if dx_l == min(dx_l, dx_r, dy_t, dy_b):
                                if node_graphic.node.enum_node != ENUM_NODE.NODE_START:
                                    node_graphic.graphic.set_is_input_knot_left(True)
                                    is_changed=True

                            if dy_t == min(dx_l, dx_r, dy_t, dy_b):
                                if node_graphic.node.enum_node != ENUM_NODE.NODE_START:
                                    node_graphic.graphic.set_is_input_knot_left(False)
                                    is_changed = True

                            if dx_r == min(dx_l, dx_r, dy_t, dy_b):
                                if node_graphic.node.enum_node != ENUM_NODE.NODE_END:
                                    node_graphic.graphic.set_is_output_knot_right(True)
                                    is_changed = True

                            if dy_b == min(dx_l, dx_r, dy_t, dy_b):
                                if node_graphic.node.enum_node != ENUM_NODE.NODE_END:
                                    node_graphic.graphic.set_is_output_knot_right(False)
                                    is_changed = True

                            if is_changed:
                                self.refresh_node(node_graphic)
                                self.refresh_node_connection(node_graphic)
                                self.project.is_changed=True
                                self.callback_on_changed()

        self.is_ctrl_press = False

    def on_canvas_drag(self, event):
        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        if self.is_drag:
            return
        self.is_drag = True
        x, y = self.canvas.get_event_coord(event)
        dx = x - self.last_canvas_click[0]
        dy = y - self.last_canvas_click[1]
        #print(f"Drag 邏輯座標: ({x}, {y})")
        #return
        #if x < 0 or y < 0:
        #    return
        # 处理画布点击事件
        self.last_canvas_click = (x, y)
        #if not self.enum_canvas_operation:
        #    print("drag_none")
        if self.enum_canvas_operation == ENUM_CANVAS_OPERATION.PAN:
            self.canvas.on_pan(event)
        if self.enum_canvas_operation and self.enum_canvas_operation == ENUM_CANVAS_OPERATION.DRAG_MOVE:
           # print("drag_move")
            #self.enum_canvas_operation = None
            node_graphic : NODE_GRAPHIC = self.get_current_node_graphic()
            if node_graphic:
                self.move_node(node_graphic, dx, dy)
                self.project.controller_node_graphic.update_node_graphic(node_graphic)

                list_node_prev= self.project.controller_node_graphic.get_node_key_by_node_key_next(self.current_node_key)

                if len(list_node_prev)>0:
                    for node_prev in list_node_prev:
                        node_key_prev = node_prev[0]
                        i = node_prev[1]
                        node_graphic_prev = self.get_node_graphic(node_key_prev)
                        output_knot_connector = node_graphic_prev.graphic.list_output_knot[i]
                        if output_knot_connector.node_key_to == self.current_node_key:
                            output_knot_connector.line_to_x +=dx
                            output_knot_connector.line_to_y += dy
                            self.canvas.delete(output_knot_connector.id_line)
                            output_knot_connector.id_line = self.draw_connection(output_knot_connector)

                            node_graphic_prev.graphic.list_output_knot[i] = output_knot_connector
                        self.project.controller_node_graphic.update_node_graphic(node_graphic_prev)
                self.project.is_changed = True
                #self.update_current_workflow_parent_graphic()
                self.update_parent_node_graphic(node_graphic)
                self.redraw_canvas()
                self.callback_on_changed()


        elif self.enum_canvas_operation and self.enum_canvas_operation ==ENUM_CANVAS_OPERATION.DRAG_CONNECT and self.current_knot_connector:
            #self.enum_canvas_operation=None
            start = self.current_knot_connector.id_line
            pressed_object, item_tags = self.smart_get_items_at_location(x, y, start)
           # print("drag_connect")

            is_found = False
            if pressed_object:
                match pressed_object:
                    case "node" | "input_knot":
                        node_key_from = self.current_knot_connector.node_key_from
                        node_from = self.project.controller_node_graphic.get_node_by_key(node_key_from)
                        node_key_to = item_tags[1]
                        node_to = self.project.controller_node_graphic.get_node_by_key(node_key_to)

                        if node_key_to != node_key_from and node_key_to != node_from.parent_key and node_from.parent_key == node_to.parent_key:
                            is_found = True

            if  is_found:
                print("draw to input")
                node_key_to = item_tags[1]
                index = self.current_knot_connector.index
                node_graphic_from = self.get_node_graphic(self.current_knot_connector.node_key_from)
                node_graphic_to = self.get_node_graphic(node_key_to)
                node_graphic_from.graphic.connect_with(self.current_knot_connector.index,
                                                       node_graphic_to.graphic)
                self.canvas.delete(self.current_knot_connector.id_line)
                if index>= len(node_graphic_from.node.list_next_node_key):
                    node_graphic_from.node.list_next_node_key.append(node_key_to)
                    node_graphic_from.graphic.list_output_knot.append(KNOT_CONNECTOR())
                else:
                    node_graphic_from.node.list_next_node_key[index] = node_key_to

                node_graphic_from.graphic.list_output_knot[index].id_line = \
                    self.draw_connection(node_graphic_from.graphic.list_output_knot[index])
                self.update_node_graphic(node_graphic_from)
                self.current_knot_connector = None
                self.enum_canvas_operation = None
                self.project.is_changed = True
               # self.callback_on_changed()
            else:
                print("draw line only")
                self.canvas.delete(self.current_knot_connector.id_line)
                self.current_knot_connector.line_to_x = x
                self.current_knot_connector.line_to_y = y
                self.current_knot_connector.id_line = self.draw_connection(self.current_knot_connector)
            self.callback_on_changed()
        self.is_drag = False

    def on_canvas_release(self, event):
        # 处理画布点击事件

        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        x, y = self.canvas.get_event_coord(event)
        if self.enum_canvas_operation == ENUM_CANVAS_OPERATION.PAN:
            self.enum_canvas_operation = None


    def smart_get_items_at_location(self, x , y, start: Optional[int] = -1)->(str, Any):
        pressed_object, item_tags = self.get_items_at_location(x, y, halo=0, start=start)
        if not pressed_object:
            pressed_object, item_tags = self.get_items_at_location(x, y, halo=5, start=start)

        return     pressed_object, item_tags

    def get_items_at_location(self, x , y, halo: Optional[int] = 0, start: Optional[int] = -1)->(str, Any):
        if start and start >=0:
            items_id = self.canvas.find_closest(x, y, halo=halo+1, start=start)
        else:
            items_id = self.canvas.find_closest(x, y, halo=halo)

        #print(f"items_id: {items_id}")
        item_id = None
        item_tags = None

        if items_id:
            for i in range(0, len(items_id)):
                if items_id[i] != "current":
                    item_id = items_id[i]
                    break

        pressed_object = None
        if item_id:
            item_tags = self.canvas.gettags(item_id)
            if self.phantom_node_graphic and self.phantom_node_graphic.key == item_tags[1]:
                return None, None
            #print(f"item_tags: {item_tags}")
            item_coord = self.canvas.coords(item_id)
            #print(f"item_coord: {item_coord}")

            if len(item_tags) > 0 and len(item_coord) >= 4:
                x1, y1, x2, y2 = map(float, item_coord[:4])

                if x1 <= x <= x2 and y1 <= y <= y2:
                    if "node" in item_tags:
                        pressed_object = "node"
                    elif "output_knot" in item_tags:
                        pressed_object = "output_knot"
                    elif "input_knot" in item_tags:
                        pressed_object = "input_knot"

                elif "connector" in item_tags:
                        pressed_object = "connector"
            elif "label" in item_tags:
                        pressed_object = "node"
        return pressed_object, item_tags



    def draw_current_node_box(self, new_current_node_key:str):
        if is_string_valid(self.current_node_key):
            node_graphic = self.project.controller_node_graphic.get_node_graphic_by_key(self.current_node_key)
            if not node_graphic:
                return
            outline_width = node_graphic.graphic.outline_width
            outline_color = node_graphic.graphic.outline_color
            self.canvas.itemconfig(node_graphic.graphic.id_body, outline = outline_color, width= outline_width)
            self.current_node_key = ""
            #self.draw_node(node_graphic)
            # Focus the new current node

        if self.current_node_key != new_current_node_key:
            self.current_node_key = new_current_node_key
            if is_string_valid(self.current_node_key):
                node_graphic = self.project.controller_node_graphic.get_node_graphic_by_key(self.current_node_key)
                outline_width = node_graphic.graphic.outline_width*2
                outline_color = "red"
                self.canvas.itemconfig(node_graphic.graphic.id_body, outline=outline_color, width=outline_width)
                if node_graphic.node.enum_node == ENUM_NODE.NODE_ITERATION:
                    self.current_workflow_iteration_key = node_graphic.key
                #self.draw_node(node_graphic)


    def handle_knot_press(self, tags):
        #Focus the connector
        #self.last_canvas_click = None
        node_graphic = self.get_node_graphic(tags[1])
        self.current_knot_connector = node_graphic.graphic.list_output_knot[int(tags[2])]

        #self.draw_connection(self.current_knot_connector, is_current=True)

    def handle_connector_press(self, tags):
        node_key = tags[1]
        index = int(tags[2])
        current_knot_connector = self.get_node_graphic(node_key).graphic.list_output_knot[index]

        if self.enum_canvas_operation and self.enum_canvas_operation == ENUM_CANVAS_OPERATION.ADD_NODE and self.enum_node_to_insert:
            new_node_key = self.insert_node()
            new_node_graphic = self.get_node_graphic(new_node_key)
            node_graphic = self.get_node_graphic(node_key)
            self.project.controller_node_graphic.insert_node_graphic_after(index, node_graphic,
                                                                               new_node_graphic)

            self.canvas.delete(current_knot_connector.id_line)
            node_graphic.graphic.list_output_knot[index].id_line = self.draw_connection(node_graphic.graphic.list_output_knot[index])
            new_node_graphic.graphic.list_output_knot[0].id_line=self.draw_connection(new_node_graphic.graphic.list_output_knot[0])
            self.project.controller_node_graphic.update_node_graphic(node_graphic)
            self.project.controller_node_graphic.update_node_graphic(new_node_graphic)
        else:
            self.current_node_key = ""
        #self.last_canvas_click = None
    def on_canvas_hover(self, event):
        if self.is_hover:
            return
        self.is_hover=True
        #x = self.canvas.canvasx(event.x)
        #y = self.canvas.canvasy(event.y)
        x, y = self.canvas.get_event_coord(event)
        #print(f"Hover 邏輯座標: ({x}, {y})")
        if self.enum_canvas_operation and self.enum_canvas_operation  in [ENUM_CANVAS_OPERATION.ADD_NODE] and self.enum_node_to_insert:
            if  self.phantom_node_graphic:
                self.phantom_node_graphic.graphic.x = x
                self.phantom_node_graphic.graphic.y = y
            else:
                node = self.project.controller_node_graphic.get_new_node(enum_node=self.enum_node_to_insert, parent_key="", is_phantom=True)
                graphic = WORKNODE_GRAPHIC(node_key=node.key)
                graphic.x = x
                graphic.y = y
                node_graphic = NODE_GRAPHIC(node=node, graphic=graphic)
                self.phantom_node_graphic = node_graphic

            self.draw_graphic(node_graphic=self.phantom_node_graphic, is_dash=True)
        self.is_hover=False
    def on_canvas_hover_end(self, event):
        if self.phantom_node_graphic:
            self.clear_graphic(self.phantom_node_graphic)
            self.phantom_node_graphic=None
        self.is_hover=False
    def delete_node_graphic(self, node_graphic: NODE_GRAPHIC, is_delete_all : Optional[bool] = False):
        node_key = node_graphic.key
        if  node_graphic.node.enum_node in [ENUM_NODE.NODE_START] and not is_delete_all:
            return

        if node_graphic.node.enum_node == ENUM_NODE.NODE_ITERATION:
            self.delete_workflow(cast(NODE_ITERATION, node_graphic.node).workflow)

        graphic = node_graphic.graphic

        for knot_connector in graphic.list_output_knot:
            if knot_connector.id_line >= 0:
                self.canvas.delete(knot_connector.id_line)

        self.clear_graphic(node_graphic)

        list_node_prev = self.project.controller_node_graphic.get_node_key_by_node_key_next(node_key)

        if len(list_node_prev) > 0:
            for node_prev_info in list_node_prev:
                node_key_prev = node_prev_info[0]
                i = node_prev_info[1]

                node_graphic_prev = self.get_node_graphic(node_key_prev)
                if node_graphic_prev:
                    self.canvas.delete(node_graphic_prev.graphic.list_output_knot[i].id_line)
                    node_graphic_prev.node.list_next_node_key[i] = ""
                    node_graphic_prev.graphic.list_output_knot[i].id_line = -1
                    node_graphic_prev.graphic.list_output_knot[i].node_key_to =""
                    self.update_node_graphic(node_graphic_prev)

        self.project.controller_node_graphic.delete_node_graphic_by_key(node_key)
        self.callback_on_node_deleted()

        #self.update_current_workflow_parent_graphic()

    def delete_workflow(self, workflow: WORKFLOW):

        dict_node_graphic = dict.copy(self.project.controller_node_graphic.dict_node_graphic)
        for node_graphic in dict_node_graphic.values():
            if node_graphic.node.parent_key == workflow.key or node_graphic.node.parent_key == workflow.parent_key:
                self.delete_node_graphic(node_graphic, is_delete_all=True)

    def on_canvas_delete(self, event):

        if self.current_node_key:
            node_graphic= self.get_current_node_graphic()

            if node_graphic.node.enum_node == ENUM_NODE.NODE_ITERATION:
                workflow = cast(NODE_ITERATION, node_graphic.node).workflow
                self.delete_workflow(workflow)
                if workflow.parent_key == self.current_workflow_iteration_key:
                    self.current_workflow_iteration_key = self.project.workflow.key

            self.delete_node_graphic(node_graphic)

            self.current_node_key = ""
            self.enum_canvas_operation = None
            self.callback_on_node_deleted()
            self.project.is_changed = True
            self.callback_on_changed()

        #elif self.current_knot_connector:
        #    node_key = self.current_knot_connector.node_key_start
        #    index = self.current_knot_connector.index
        #    node_graphic = self.get_node_graphic(node_key)
        #    self.canvas.delete(node_graphic.graphic.list_output_knot[index].id_line)
        #    node_graphic.graphic.list_output_knot[index] = KNOT_CONNECTOR()
        #    self.update_node_graphic(node_graphic)
        #    self.current_knot_connector = None


class Node_Configer_Base():
    def __init__(self, parent: TK_WINDOW, callback:Callable, translator: Optional[LanguageTranslator]=None, node:Optional[Any]=None):
        super().__init__()
        self.node = node
        self.parent = parent
        self.callback = callback
        self.translator = translator
        self.root = None

    def  grid(self, width:Optional[float]=None, height:Optional[float] = None, ** kwargs):
        args={}
        if width and isinstance(width, float):
            args['width']=width

        if height and isinstance(height, float):
            args['height'] = height

        self.root = tk.Frame(self.parent, args)
        self.root.grid(kwargs)
        self.build_ui()
        return self

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        print("build ui")

class Node_Configer():
    def __init__(self, parent: TK_WINDOW,
                 callback_node_changed:Callable,
                 callback_name_changed:Callable,
                 translator: LanguageTranslator,
               #  llms_api: Optional[LLMS_API] = None,
                 list_embed_model_name: Optional[List[str]]=None,
                # settings_knowledge_collections: Optional[KNOWLEDGE_COLLECTIONS]=None
                 ):
        super().__init__()
        self.project_page = None
      #  self.global_variables = None
       # self.workflow = self.project_page.project.controller_node_graphic.get_node_graphic_by_key(self.project_page.current_workflow_key).work_node

        self.translator : LanguageTranslator = translator
       # self.llms_api = llms_api
        self.list_embed_model_name = list_embed_model_name
       # self.settings_knowledge_collections = settings_knowledge_collections
        self.callback_node_changed=callback_node_changed
        self.callback_name_changed = callback_name_changed
        self.controller_node_graphic = None
        self.parent = parent
        self.root = None
        self.content_frame = None  # 動態內容容器
        self.node = None
        self.current_configer = None
        #self.window_geometry = None
        self.label_title: Optional[ttk.Label]=None
        self.editor_name: Optional[Text_Editor]=None


    def set_node(self, node: WORK_NODE, project_page: PROJECT_PAGE):
        if not node or not project_page:
            return

        self.node = copy(node)
        self.project_page = project_page
       # self.llms_api = project_page.project.llms_api
       # self.set_node_llms_api()

        self.controller_node_graphic : CONTROLLER_NODE_GRAPHIC = project_page.project.controller_node_graphic
        #self.global_variables = self.project_page.project.global_variables
        if not self.root:
            self._create_window()  # 首次創建窗口
        else:
            self._update_window()  # 更新已有窗口
        self._build_ui()


    def _create_window(self):
        if not self.parent.winfo_exists():
            raise RuntimeError("父窗口已被銷毀，無法創建配置窗口")
        self.root = ttk.Frame(self.parent)
        self.root.pack(fill="both", expand=True)

        self.root.focus_set()
        # 窗口尺寸限制
        #self.root.minsize(200, 200)
        #self.root.protocol("WM_DELETE_WINDOW", self._on_close)  # 綁定關閉事件
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _center_window(self):
        """ 居中窗口於父窗口 """
        self.root.update_idletasks()  # 確保窗口尺寸已計算
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()

        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        x = parent_x + (parent_width - window_width) // 2
        y = parent_y + (parent_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")

    def _on_close(self):
        #self.window_geometry = self.root.geometry()
        self.destroy()

    def clear(self):
        self.destroy()

    def destroy(self):
        if self.current_configer:
            self.current_configer.destroy()
        self.current_configer = None
        if self.root:
            self.root.destroy()
            self.root = None  # 清除引用避免野指針
        self.node = None

    def _update_window(self):
        # 清空舊內容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        #self.root.title(f"属性编辑 - {self.node.name}")

    def on_name_changed(self, new_name):
        if not self.controller_node_graphic.is_node_key_existed(new_name):
            old_key = self.node.key
            self.controller_node_graphic.change_name(old_key, new_name)
            self.node=self.controller_node_graphic.get_node_by_key(new_name)
            #self.root.title(f"属性编辑 - {self.node.name}")  # 實時更新標題
            self.callback_name_changed(self.node)
        else:
            messagebox.showwarning(self.translator.get_translation("warning"),
                                   self.translator.get_translation("node_name_existed")+":"+new_name)

    def on_node_changed(self, node: WORK_NODE):
        self.node = node
        self.callback_node_changed(self.node)

    def refresh(self):
        if self.label_title and self.node and self.node.enum_node :
            self.label_title.configure(text=self.translator.get_translation("node_type") +f":{self.node.enum_node.value}")
        if self.editor_name:
            self.editor_name.configure(label=self.translator.get_translation("node_name"))
        if self.current_configer:
            self.current_configer.refresh()


    def _build_ui(self):
        self.label_title = ttk.Label(self.content_frame, text=self.translator.get_translation("node_type") +f":{self.node.enum_node.value}")
        self.label_title.grid(row=0, column=0)
        self.editor_name = Text_Editor(self.content_frame, var=self.node.name, callback=self.on_name_changed,
                                       label=self.translator.get_translation("node_name"),
                                       ).grid(row=1, column=0, field_width=30, sticky="w")

        next_row = 2

        if self.current_configer:
            self.current_configer.destroy()

        match self.node.enum_node:
            case ENUM_NODE.NODE_END:
                self.current_configer = Configer_NODE_END(self.node, parent=self.content_frame, callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_ITERATION:
                self.current_configer = Configer_NODE_ITERATION(self.node, parent=self.content_frame, callback=self.on_node_changed,
                                                                # global_variables=self.global_variables,
                                                                translator=self.translator).grid(row=next_row)
            case ENUM_NODE.NODE_BRANCH:
                self.current_configer = Configer_NODE_BRANCH(self.node, parent=self.content_frame, callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_PYTHON_CODE_EXECUTOR:
                self.current_configer = Configer_NODE_PYTHON_CODE_EXECUTOR(self.node, parent=self.content_frame,
                                                                           # global_variables=self.global_variables,
                                                                           callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_ASK_LLM:
                self.current_configer = Configer_NODE_ASK_LLM(self.node, parent=self.content_frame,
                                                              callback=self.on_node_changed,
                                                              #llms_api=self.llms_api,
                                                              # global_variables=self.global_variables,
                                                              translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_CATEGORIZED_BY_LLM:
                self.current_configer = Configer_NODE_CATEGORIZE_BY_LLM(self.node, parent=self.content_frame, callback=self.on_node_changed,
                                                                       # llms_api=self.llms_api,
                                                                        #  global_variables=self.global_variables,
                                                                        translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_KNOWLEDGE_RETRIEVER:
                self.current_configer = Configer_NODE_KNOWLEDGE_RETRIEVER(self.node, parent=self.content_frame, callback=self.on_node_changed,
                                                                         # llms_api=self.llms_api,
                                                                          #  list_embed_model_name=self.list_embed_model_name,
                                                                          #    global_variables=self.global_variables,
                                                                          knowledge_collections=self.project_page.project.knowledge_collections, translator=self.translator).grid(row=next_row)
           #case ENUM_NODE.NODE_ASK_LLM_WITH_KNOWLEDGE:
           #    self.current_configer = Configer_NODE_ASK_LLM_WITH_KNOWLEDGE(self.node, parent=self.content_frame, callback=self.on_node_changed,
           #                                                                # llms_api=self.llms_api,
           #                                                                 # global_variables=self.global_variables,
           #                                                                 translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_SEND_MAIL:
                self.current_configer = Configer_NODE_SEND_MAIL(self.node, parent=self.content_frame, callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_RECEIVE_MAIl:
                self.current_configer = Configer_NODE_RECEIVE_MAIL(self.node, parent=self.content_frame,
                                                                callback=self.on_node_changed,
                                                                translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_HTTP_REQUEST:
                self.current_configer = Configer_NODE_HTTP_REQUEST(self.node, parent=self.content_frame, callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_FTP_UPLOAD:
                self.current_configer = Configer_NODE_FTP_UPLOAD(self.node, parent=self.content_frame,
                                                                 callback=self.on_node_changed,
                                                                 translator=self.translator).grid(row=next_row)
            case ENUM_NODE.NODE_SFTP_UPLOAD:
                self.current_configer = Configer_NODE_SFTP_UPLOAD(self.node, parent=self.content_frame,
                                                                 callback=self.on_node_changed,
                                                                 translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_CRAWL:
                self.current_configer =  Configer_NODE_CRAWL(self.node, parent=self.content_frame, callback=self.on_node_changed, translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_EXTRACT_TEXT:
                self.current_configer = Configer_NODE_EXTRACT_TEXT(self.node, parent=self.content_frame,
                                                            callback=self.on_node_changed,
                                                            translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_OCR:
               self.current_configer = Configer_NODE_OCR(self.node, parent=self.content_frame, callback=self.on_node_changed,
                                                       translator=self.translator).grid(row=next_row)

            case ENUM_NODE.NODE_VOICE_RECOGNIZE:
                self.current_configer = Configer_NODE_VOICE_RECOGNIZE(self.node, parent=self.content_frame,
                                                          callback=self.on_node_changed,
                                                          translator=self.translator).grid(row=next_row)
            case ENUM_NODE.NODE_GENERATE_IMAGE_FROM_TEXT:
                self.current_configer = Configer_NODE_GENERATE_IMAGE_FROM_TEXT(self.node, parent=self.content_frame,
                                                                               callback=self.on_node_changed,
                                                                               translator=self.translator).grid(row=next_row)
            case ENUM_NODE.NODE_TRANSLATED_BY_LLM:
                self.current_configer = Configer_NODE_TRANSLATED_BY_LLM(self.node, parent=self.content_frame,
                                                                       # llms_api=self.llms_api,
                                                                        callback=self.on_node_changed,
                                                                        translator=self.translator).grid(
                    row=next_row)

        #case _:
            #    raise ValueError(f"未知的節點類型: {self.node.enum_node}")


class Configer_NODE_ITERATION(Node_Configer_Base):
    def __init__(self, node: NODE_ITERATION, parent: TK_WINDOW, translator: LanguageTranslator, callback:Callable):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_ITERATION, node)
        self.combo_source = node.global_variables.get_list_array_name()
        self.id_label: Optional[ttk.Label]=None
        self.editor: Optional[Combo_Text_Editor] = None

        if not self.combo_source or len(self.combo_source) == 0:
            raise ValueError(f"未知的節點類型: {self.node.enum_node}")


    def on_array_name_changed(self, new_name):
        self.node.set_array_name(new_name)
        self.callback(self.node)

    def on_item_name_changed(self, new_name):
        self.node.set_item_name(new_name)
        self.callback(self.node)

    def on_item_index_name_changed(self, new_name):
        self.node.set_item_index_name(new_name)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()
    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        if not self.node.array_name:
            self.on_array_name_changed(self.combo_source[0])

        Combo_Text_Editor(self.root, var=self.node.array_name,
                          callback=self.on_array_name_changed,
                                label=self.translator.get_translation("array_name"),
                          combo_source=self.node.global_variables.get_list_array_name(),
                          ).grid(row=1, column=0)

        Combo_Text_Editor(self.root, var=self.node.item_name,
                          callback=self.on_item_name_changed,
                                label=self.translator.get_translation("item_name"),
                          combo_source=self.node.global_variables.get_list_key(),
                              ).grid(row=2, column=0)

        Combo_Text_Editor(self.root, var=self.node.item_index_name,
                          callback=self.on_item_index_name_changed,
                          label=self.translator.get_translation("item_index_name"),
                                combo_source=self.node.global_variables.get_list_key(),
                          ).grid(row=3, column=0)

class Configer_NODE_BRANCH(Node_Configer_Base):
    def __init__(self, node: NODE_BRANCH, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_BRANCH, node)

        self.edit_number_branches: Optional[Text_Editor] = None
        self.ttk_label : Optional[ttk.Label] = None

    def on_number_changed(self, new_text: str):
        # 獲取當前輸入框的內容
        if new_text and len(new_text)>0:
            new_number = int(new_text)
            if new_number > 0:
                self.node.set_number_of_branches(new_number)
                self.callback(self.node)
            else:
                messagebox.showwarning(self.translator.get_translation("warning"), self.translator.get_translation("must_be_positive_integer"))

    def on_index_branch_name_changed(self, new_name):
        self.node.set_index_branch_name(new_name)
        self.callback(self.node)

    def on_evaluator_code_changed(self, new_evaluator):
        self.node.set_evaluator_code(new_evaluator)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()
    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        self.edit_number_branches = Text_Editor(self.root, var=str(self.node.number_of_branches), callback=self.on_number_changed,
                                                label=self.translator.get_translation("number_branches"),
                                                ).grid(row=1, column=0)
        Text_Editor(self.root, var=self.node.index_branch_name,
                    callback=self.on_index_branch_name_changed,
                          label=self.translator.get_translation("index_branch_variable"),
                          ).grid(row=2, column=0, field_width=30)

        self.ttk_label=ttk.Label(self.root, text=self.translator.get_translation("evaluator_code"))
        self.ttk_label.grid(row=3, column=0, columnspan=2, sticky="w")

        Scroll_Text_Editor(self.root, var=self.node.evaluater_code, callback=self.on_evaluator_code_changed,
                          ).grid( row=4, column=0, columnspan=2)


class Configer_NODE_END(Node_Configer_Base):
    def __init__(self, node: NODE_END, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator
                ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_END, node)

    def on_is_publish_changed(self, is_publish: bool):
        self.node.set_is_publish(is_publish)
        self.callback(self.node)

    def on_answer_composer_changed(self, answer_composer: str):
        self.node.set_answer_composer(answer_composer)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str] = None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        ttk_title = ttk.Label(self.root, text=self.translator.get_translation("answer_composer"))
        ttk_title.grid(row=1, column=0, sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.answer_composer, callback=self.on_answer_composer_changed).grid(row=2, column=0)
        Combo_Text_Editor(self.root, var=self.node.output_variables_key[0],
                          callback=self.on_output_variable_key_changed,
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                          is_nullable=True,
                          null_str=self.translator.get_translation("none"),
                               ).grid(row=3, column=0)
        CheckBox_Editor(self.root, var=self.node.is_publish,
                        callback=self.on_is_publish_changed,
                        label=self.translator.get_translation("is_publish"),
                        ).grid(row=4, column=0)


class Configer_NODE_PYTHON_CODE_EXECUTOR(Node_Configer_Base):
    def __init__(self, node: NODE_PYTHON_CODE_EXECUTOR, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator
                ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
    #    super().__init__()
    #    self.node = node
    #    self.parent = parent
    #    self.root = None
    #    self.callback = callback
    #    self.translator = translator
#
     #   self.combo_source = global_variables.get_list_key()
#
    #def grid(self, row: int = 0, column: int = 0, columnspan: int = 1, padx: int = 1, pady: int = 1,
    #         sticky: str = "w") -> "Config_NODE_PYTHON_CODE_EXECUTOR":
#
    #    self.root = tk.Frame(self.parent)
    #    self.root.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
    #    self.build_ui()
    #    return self
#
    #def destroy(self):
    #    destroy_TK_WINDOW(self.root)
        self.ttk_label_code: Optional[ttk.Label] = None
        self.ttk_label_output_variables_key: Optional[ttk.Label] = None
        self.node = cast(NODE_PYTHON_CODE_EXECUTOR, node)

    def on_list_changed(self, list_text: [str], enum_edit: Enum_Edit, index: int):
        self.node.set_output_variables_key(list_text)
        self.callback(self.node)

    def on_code_changed(self, new_code: str):
        self.node.set_code(new_code)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="w")
        self.ttk_label_output_variables_key = ttk.Label(frame,
                                                        text=self.translator.get_translation("output_variables_key"))
        self.ttk_label_output_variables_key.grid(row=0, column=0)

        List_Editor_Combo(frame, var=self.node.output_variables_key,
                               callback=self.on_list_changed,
                               combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=1, column=1)
        self.ttk_label_code=ttk.Label(self.root, text=self.translator.get_translation("code"))
        self.ttk_label_code.grid(row=2, column=0, sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.evaluater_code, callback=self.on_code_changed).grid(row=3, column=0)

import threading
class Editor_KNOWLEDGE_COLLECTION(Node_Configer_Base):
    def __init__(self, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,
                 knowledge_collection: KNOWLEDGE_COLLECTION,
                 settings_knowledge_collections:Optional[ KNOWLEDGE_COLLECTIONS]=None,
                # server_mount_base_path: Optional[str] = None
                 ):
        super().__init__( parent=parent, callback=callback, translator=translator)
        #super().__init__()
        #self.parent = parent
        #self.callback = callback
        #self.translator = translator
        #self.root = None

        self.knowledge_collection: KNOWLEDGE_COLLECTION = knowledge_collection
        self.settings_knowledge_collections: KNOWLEDGE_COLLECTIONS= settings_knowledge_collections
        self.knowledge_collection_name_selected: Optional[str] = None
        #self.list_collection_name = None
        self.settings_collection_name=None
        #self.server_mount_base_path = server_mount_base_path

        #if self.settings_knowledge_collections:
        #    self.list_collection_name= self.settings_knowledge_collections.get_list_collection_name()

        self.label_title: Optional[ttk.Label]=None
        self.selector_settings_collection_names: Optional[Combo_Text_Editor]= None
        self.button_copy: Optional[ttk.Button]=None
        self.button_vectorize: Optional[ttk.Button] = None
        self.editor_collection_name: Optional[Text_Editor]=None
        self.editor_description:Optional[Text_Editor]=None
        self.label_files_path: Optional[ttk.Label]=None
        self.selector_list_filepath:Optional[List_Selector_Filepath]=None
        self.editor_chunk_size: Optional[Text_Editor]=None
        self.editor_chunk_overlap:Optional[Text_Editor]=None
        self.selector_embed_model:Optional[Combo_Text_Editor]=None
        self.label_persist_directory: Optional[ttk.Label]=None
        self.selector_filepath: Optional[Filepath_Selector]=None

        self.processing_started = False
        self.processing_completed = False
        self.processing_window = None
        self.completion_window = None
        self.status_label = None


    def on_collection_name_changed(self, collection_name: str):
        self.knowledge_collection.set_collection_name(collection_name)
        self.callback(self.knowledge_collection)

    def on_description_changed(self, description: str):
        self.knowledge_collection.set_description(description)
        self.callback(self.knowledge_collection)

    def on_enum_storage_type_changed(self, enum_storage_type: ENUM_STORAGE_TYPE):
        self.knowledge_collection.is_vectorized = False
        self.knowledge_collection.set_enum_storage_type(enum_storage_type)
        self.callback(self.knowledge_collection)
        self.build_ui()

    def on_knowledge_files_path_changed(self, knowledge_files_path: [str], enum_edit: Enum_Edit, i: int):
        self.knowledge_collection.is_vectorized = False
        self.knowledge_collection.set_knowledge_files_path(knowledge_files_path)
        self.callback(self.knowledge_collection)

    def on_chunk_size_changed(self, chunk_size_str: str):
        self.knowledge_collection.is_vectorized = False
        self.knowledge_collection.set_chunk_size(int(chunk_size_str))
        self.callback(self.knowledge_collection)

    def on_chunk_overlap_changed(self, chunk_overlap_str: str):
        self.knowledge_collection.is_vectorized = False
        self.knowledge_collection.set_chunk_overlap(int(chunk_overlap_str))
        self.callback(self.knowledge_collection)

    def on_embed_model_name_changed(self, embed_model_name: str):
        self.knowledge_collection.is_vectorized = False
        self.knowledge_collection.set_embed_model_name(embed_model_name)
        self.callback(self.knowledge_collection)

    def on_persist_directory_changed(self, persist_directory: str):
        self.knowledge_collection.is_vectorized=False
        self.knowledge_collection.set_persist_directory(persist_directory)
        self.callback(self.knowledge_collection)

    def on_is_persist_at_server_changed(self, is_persist_at_server: bool):
        self.knowledge_collection.set_is_persist_at_server(is_persist_at_server)
        self.callback(self.knowledge_collection)
        self.build_ui()

    def on_server_url_changed(self, server_url: str):
        self.knowledge_collection.set_server_url(server_url)
        self.callback(self.knowledge_collection)

    def on_project_name_changed(self, project_name: str):
        self.knowledge_collection.set_project_name(project_name)
        self.callback(self.knowledge_collection)

   # def on_application_changed(self, application: str):
   #     self.knowledge_collection.is_vectorized = False
   #     self.knowledge_collection.set_application(application)
   #     self.callback(self.knowledge_collection)

    #def on_settings_collection_name_changed(self, collection_name:str):
    #    self.settings_collection_name= collection_name

    def on_selector_settings_knowledge_collections_changed(self, key: str):
        if key:
            self.knowledge_collection_name_selected = key

    def on_button_copy_clicked(self):
        if self.knowledge_collection_name_selected:
            self.knowledge_collection = deepcopy( self.settings_knowledge_collections.get_item_by_key(self.knowledge_collection_name_selected))
            self.callback(self.knowledge_collection)
            destroy_TK_WINDOW(self.root, is_destroy_root=False)
            self.build_ui()

    def on_button_vectorize_clicked(self):
        #self.knowledge_collection.vectorize()
        if self.processing_started:
            return

        if (not is_string_valid(self.knowledge_collection.persist_directory) or
            not is_string_valid(self.knowledge_collection.collection_name) or
             len(self.knowledge_collection.knowledge_files_path)<=0) :
            return
        self.processing_started = True
        self.show_processing_window()

        # 在新线程中执行向量化操作
        processing_thread = threading.Thread(
            target=self.execute_vectorization,
            daemon=True
        )
        processing_thread.start()

    def execute_vectorization(self):
        """执行向量化操作"""
        try:
            self.knowledge_collection.vectorize()
            self.processing_completed = True
            # 完成后回到主线程更新UI
            self.root.after(0, self.show_completion_window)
        except Exception as e:
            # 错误处理 - 保存错误信息到实例变量
            self.last_error = str(e)
            # 使用实例变量而不是捕获变量
            self.root.after(0, self.show_error_window)
        finally:
            self.processing_started = False

    def show_processing_window(self):
        """显示处理中提示窗口"""
        if self.processing_window:
            self.processing_window.destroy()

        self.processing_window = get_new_center_window(self.root, window_width=300, window_height=100)
        #print(f'root_x={self.root.winfo_x()}')
        self.processing_window.title(self.translator.get_translation("vectorization"))

        # 窗口内容
        self.status_label=ttk.Label(
            self.processing_window,
            text=self.translator.get_translation("vectorizing")+self.knowledge_collection.collection_name,
            font=("Arial", 11),
            justify="center"
        )
        self.status_label.pack(expand=True, fill="both", padx=20, pady=10)

        # 3秒后自动关闭
       # self.processing_window.after(3000, self.close_processing_window)

    def close_processing_window(self):
        """关闭处理中窗口"""
        if self.processing_window:
            self.processing_window.grab_release()
            self.processing_window.destroy()
            self.processing_window = None

    def show_completion_window(self):
        self.status_label.config(text= self.translator.get_translation(
            "vectorization_completed") + ' - ' + self.knowledge_collection.collection_name)
        self.processing_window.after(3000, self.close_processing_window)

    def show_completion_window_old(self):
        """显示处理完成窗口"""
        if not self.processing_completed:
            return

        #self.close_processing_window()  # 确保关闭之前的窗口

        self.completion_window = get_new_center_window(self.root, window_width=300, window_height=100)
        self.completion_window.title(self.translator.get_translation("vectorization"))

        # 窗口内容
        ttk.Label(
            self.completion_window,
            text=self.translator.get_translation("vectorization_completed")+' - '+self.knowledge_collection.collection_name,
            font=("Arial", 11),
            justify="center",
            foreground="green"
        ).pack(expand=True, fill="both", padx=20, pady=10)

        self.callback(self.knowledge_collection)
        # 3秒后自动关闭
        self.completion_window.after(3000, self.close_completion_window)

    def close_completion_window(self):
        """关闭完成窗口"""
        if self.completion_window:
            self.completion_window.grab_release()
            self.completion_window.destroy()
            self.completion_window = None
            self.processing_completed = False

    def show_error_window(self):
        """显示错误窗口 - 使用实例变量获取错误信息"""
        error_msg = self.last_error if hasattr(self, 'last_error') else "Unknown error"
        self.close_processing_window()

        error_window = get_new_center_window(self.root, window_width=400, window_height=150)
        error_window.title(self.translator.get_translation("error"))

        # 错误信息
        ttk.Label(
            error_window,
            text=self.translator.get_translation("error"),
            font=("Arial", 11),
            justify="center",
            foreground="red"
        ).pack(padx=20, pady=10)

        # 具体错误详情
        ttk.Label(
            error_window,
            text=error_msg,
            font=("Arial", 9),
            wraplength=380,
            justify="center"
        ).pack(padx=20, pady=5)

        # 关闭按钮
        ttk.Button(
            error_window,
            text=self.translator.get_translation("close"),
            command=error_window.destroy
        ).pack(pady=10)

        # 确保窗口居中
        #self.center_window(error_window)

    def center_window(self, window):
        """使窗口居中显示"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        index_row = 0
        self.label_title = ttk.Label(self.root, text=self.translator.get_translation("knowledge_collection"), style="Config_Title.TLabel")
        self.label_title.grid(row=index_row, column=0)
        index_row += 1
        if self.settings_knowledge_collections and self.settings_knowledge_collections.length()>0:
            self.selector_settings_collection_names = (Combo_Text_Editor(self.root, var="",
                                                                         callback=self.on_selector_settings_knowledge_collections_changed,
                                                                              label=self.translator.get_translation("settings_collection_names"),
                                                                              combo_source=self.settings_knowledge_collections.get_list_collection_name(),
                                                                              ).
                                                       grid(row=index_row, column=0, ))

            self.button_copy=ttk.Button(self.root, text=self.translator.get_translation("copy"), command= self.on_button_copy_clicked)
            self.button_copy.grid(row=index_row, column= 1, padx=1, sticky="w")
            index_row += 1
            self.knowledge_collection_name_selected = self.settings_knowledge_collections.get_list_collection_name()[0]

        self.editor_collection_name = Text_Editor(self.root, var=self.knowledge_collection.collection_name,
                                                        label= self.translator.get_translation("collection_name"),
                                                        callback=self.on_collection_name_changed).grid(row=index_row, column=0, field_width=30)
        index_row += 1
        self.editor_description = Text_Editor(self.root, var=self.knowledge_collection.description,
                                                    label=self.translator.get_translation("description"),
                                                    callback=self.on_description_changed).grid(row=index_row, column=0, field_width=50)

        #index_row += 1
        #Text_Editor(self.root, text=self.knowledge_collection.project_name,
        #                                      label=self.translator.get_translation("project_name"),
        #                                      callback=self.on_project_name_changed).grid(row=index_row, column=0,
        #                                                                                 width=50)

        index_row += 1
        list_storage_type_value = [member.value for member in ENUM_STORAGE_TYPE]
        Combo_Text_Editor(self.root, var = self.knowledge_collection.enum_storage_type.value,
                          callback=self.on_enum_storage_type_changed,
                          label=self.translator.get_translation("storage_type"),
                           combo_source=list_storage_type_value).grid(row=index_row, column=0)
        index_row += 1

        frame_list_filepath_selector = ttk.Frame(self.root)
        frame_list_filepath_selector.grid(row=index_row, column=0, sticky="w")
        index_row += 1

        self.label_files_path = ttk.Label(frame_list_filepath_selector, text=self.translator.get_translation("files_path"))
        self.label_files_path.grid(row=0, column=0)

        self.selector_list_filepath = List_Selector_Filepath(frame_list_filepath_selector, var=self.knowledge_collection.knowledge_files_path,
                                                             callback=self.on_knowledge_files_path_changed, label_for_button_pick=self.translator.get_translation("pick"),
                                                            # server_url=self.server_mount_base_path
                                                             ).grid(row=0, column=1)

        list_embed_model = list(get_args(EMBED_MODELS))
        if not self.knowledge_collection:
            self.on_embed_model_name_changed(list_embed_model[0])

        self.selector_embed_model = Combo_Text_Editor(self.root, var=self.knowledge_collection.embed_model_name,
                                                      callback=self.on_embed_model_name_changed,
                                label=self.translator.get_translation("embed_model"),
                          combo_source=list_embed_model,
                          ).grid( row=index_row, column=0, field_width=40)

        #index_row += 1
        #frame_filepath_selector = ttk.Frame(self.root)
        #frame_filepath_selector.grid(row=index_row, column=0, sticky="w")
        index_row += 1
        CheckBox_Editor(self.root,
                        var=self.knowledge_collection.is_persist_at_server,
                        callback=self.on_is_persist_at_server_changed,
                        label=self.translator.get_translation("is_persist_at_server"),
                       ).grid(row=index_row, column=0)

        index_row += 1
        self.selector_filepath = Filepath_Editor(self.root,
                                                 var=self.knowledge_collection.persist_directory,
                                                 callback=self.on_persist_directory_changed,
                                                 label=self.translator.get_translation("persist_directory"),
                                                 is_dir=True, is_pick= not self.knowledge_collection.is_persist_at_server,
                                                   label_for_button_pick=self.translator.get_translation("pick"),
                                                   #server_url=self.server_mount_base_path
                                                   ).grid(row=index_row, column=0, field_width=50)
        if self.knowledge_collection.is_persist_at_server:
            index_row += 1
            Text_Editor(self.root, var=self.knowledge_collection.server_url,
                        callback=self.on_server_url_changed,
                                                label=self.translator.get_translation("wofa_server_url"),
                                                ).grid(row=index_row, column=0, field_width=50)
        index_row += 1
        if self.knowledge_collection.enum_storage_type == ENUM_STORAGE_TYPE.CHUNK:
            self.editor_chunk_size = Text_Editor(self.root, var=str(self.knowledge_collection.chunk_size),
                                                 callback=self.on_chunk_size_changed,
                                                 label=self.translator.get_translation("chunk_size"),
                                                 ).grid(row=index_row, column=0)
            index_row += 1
            self.editor_chunk_overlap = Text_Editor(self.root, var=str(self.knowledge_collection.chunk_overlap),
                                                    callback=self.on_chunk_overlap_changed,
                                                    label=self.translator.get_translation("chunk_overlap"),
                                                   ).grid(  row=index_row, column=0)
            index_row += 1
        ttk.Button(self.root, text=self.translator.get_translation("vectorize"), command=self.on_button_vectorize_clicked
                   ).grid(row=index_row, column= 0, padx=1, sticky="w")

class Editor_KNOWLEDGE_COLLECTIONS(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable,
                 translator: LanguageTranslator,items: Optional[KNOWLEDGE_COLLECTIONS] = None,
                 settings_knowledge_collections:Optional[ KNOWLEDGE_COLLECTIONS]=None,
                 ):
        super().__init__( parent=parent, callback=callback, translator=translator)
        #super().__init__()
        #self.callback = callback
        #self.translator = translator
        #self.root = None

        self.new_items = items if items else KNOWLEDGE_COLLECTIONS()
        self.settings_knowledge_collections : KNOWLEDGE_COLLECTIONS=settings_knowledge_collections

        self.list_new_item: List[KNOWLEDGE_COLLECTION] = self.new_items.get_list_item()
        self.list_new_key = [item.collection_name for item in self.list_new_item]
        self.list_is_expanded: List[bool] = [False] * len(self.list_new_key) if len(self.list_new_key) > 0 else []
        self.name_manager = NAME_MANAGER()
        if len(self.list_new_key)>0:
            for name in self.list_new_key:
                self.name_manager.add_name(name=name)

        self.list_button_minus: List[ttk.Button] = []
        self.list_button_plus: List[ttk.Button] = []
        #self.list_button_expand_collapse: List[ttk.Button] = []
        #self.list_editor: List[Editor_KNOWLEDGE_COLLECTION] = []
        self.label_title: Optional[ttk.Label]=None
        self.parent = parent
        self.parent_row = 0
        self.parent_column = 0

        self.row = 0
        self.column = 0

        self.top = None
        self.canvas = None
        self.scroll_position = None
        self.build_ui()

    #ef grid(self, row: int = 0, column: int = 0, columnspan: int = 1, padx: int = 1, pady: int = 1,
    #        sticky: str = "w") -> "Editor_KNOWLEDGE_COLLECTION":

    #   self.parent_row = row
    #   self.parent_column = column
    #   self.parent_sticky = sticky

    #   self.row = 0
    #   self.column = 0
    #   self.columnspan = columnspan
    #   self.root = None
    #   self.build_ui()
    #   return self

    def lift(self):
        if self.top:
            if self.top.state() == 'iconic':
                self.top.deiconify()
            self.top.lift()
        else:
            self.build_ui()

    def on_item_changed(self, new_item: KNOWLEDGE_COLLECTION, i):
        #new_variable = self.list_editor[i].variable
        self.list_new_key[i] = new_item.collection_name
        self.list_new_item[i] = new_item
        self.new_items.set_list_item(self.list_new_item)
        self.callback(self.new_items)

    def click_minus(self, index: int):
        if 0 <= index < len(self.list_new_key):
            self.list_new_item.pop(index)
            self.list_new_key.pop(index)
            self.list_is_expanded.pop(index)
            self.new_items.set_list_item(self.list_new_item)

            self.build_ui()
            self.callback(self.new_items)

    def click_plus(self, i: int):
        if 0 <= i <= self.new_items.length():
            name = self.name_manager.get_new_name(name="knowledge_collection")
            item = KNOWLEDGE_COLLECTION(collection_name=name)
            if i < self.new_items.length():
                self.list_new_item.insert(i, item)
                self.list_new_key.insert(i, name)
                self.list_is_expanded.insert(i, False)
            else:
                self.list_new_item.append(item)
                self.list_new_key.append(name)
                self.list_is_expanded.append(False)
            self.new_items.set_list_item(self.list_new_item)
            self.build_ui()

            self.callback(self.new_items)

    def click_expand_collapse(self, i: int):
        self.list_is_expanded[i] = not self.list_is_expanded[i]
        self.build_ui()

    def count_expand(self) -> int:
        count = 0
        for is_expand in self.list_is_expanded:
            if is_expand:
                count += 1
        return count

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.canvas=None
        self.top = None

    def build_ui(self):
        size_of_list = len(self.list_new_key)
        if self.canvas:
            self.scroll_position = self.canvas.yview()
        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 700
        top_height = 400
        self.top.geometry(f"{top_width}x{top_height}")
        #self.top.attributes("-topmost", True)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + parent_width - top_width
        y = self.parent.winfo_y() + 50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = screen_width - top_width
        # 應用幾何位置
        self.top.geometry(f"{top_width}x{top_height}+{x}+{y}")

        self.canvas = tk.Canvas(self.top)
        scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=self.canvas.yview)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 配置 Canvas 的垂直滾動
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.root, anchor="nw")

        # 綁定 Frame 大小變化時更新滾動區域
        def update_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.root.bind("<Configure>", update_scrollregion)
        style = ttk.Style()
        style.configure("Narrow.TButton", width=2)

        self.row = 0
        self.label_title =ttk.Label(self.root, text=self.translator.get_translation("knowledge_collection_editor"), style="Config_Title.TLabel")
        self.label_title.grid(row=0, column=0, columnspan=4)
        self.row += 1
        for i in range(0, size_of_list + 1):
            button_plus = ttk.Button(self.root, width=2, text="+", command=lambda idx=i: self.click_plus(idx))
            button_plus.grid(row=self.row + 2*i , column=self.column + 1, padx=1, sticky="w")
            self.list_button_plus.append(button_plus)
            if i < size_of_list:
                button_minus = ttk.Button(self.root, width=2, text="-", command=lambda idx=i: self.click_minus(idx))
                button_minus.grid(row=self.row + 2*i , column=self.column, padx=1, sticky="w")
                self.list_button_minus.append(button_minus)

                editor = None
                if self.list_is_expanded[i]:
                    editor = Editor_KNOWLEDGE_COLLECTION(self.root, knowledge_collection=self.new_items.get_item_by_key(self.list_new_key[i]),
                                                         callback=lambda item, current_i=i: self.on_item_changed(item, current_i),
                                                         translator=self.translator,
                                                         settings_knowledge_collections=self.settings_knowledge_collections,
                                                         )
                    editor.grid(row=self.row + 2*i , column=self.column + 2, sticky="w")
                    button_text = "<"
                else:
                    key = self.list_new_key[i]
                    knowledge_collection = self.new_items.get_item_by_key(key)
                    editor = ttk.Label(self.root, text=self.new_items.get_item_by_key(self.list_new_key[i]).collection_name)
                    editor.grid(row=self.row + 2*i , column=self.column + 2, sticky="w")
                    button_text = ">"
                button = ttk.Button(self.root, width=2, text=button_text,
                                    command=lambda idx=i: self.click_expand_collapse(idx))
                button.grid(row=self.row + 2*i , column=self.column + 3 , padx=1, sticky="e")
                #self.list_button_expand_collapse.append(button)
                #self.list_editor.append(editor)
                separator = ttk.Separator(self.root, orient="horizontal")
                separator.grid(row=self.row + 2*i+1, column=0, columnspan=4, sticky="ew", pady=5)


        if self.scroll_position:
            _scroll_to = self.scroll_position[0]
        else:
            _scroll_to = 1.0
        self.canvas.yview_moveto(_scroll_to)
        self.canvas.after(100, lambda: self.canvas.yview_moveto(_scroll_to))


class Picker_KNOWLEDGE_COLLECTIONS(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable, callback_settings: Callable,
                 translator: LanguageTranslator, items: Optional[KNOWLEDGE_COLLECTIONS] = None,
                 settings_knowledge_collections:Optional[ KNOWLEDGE_COLLECTIONS]=None):
        super().__init__( parent=parent, callback=callback, translator=translator)

        self.settings_knowledge_collections : KNOWLEDGE_COLLECTIONS=settings_knowledge_collections
        self.list_key = items.get_list_collection_name()

        self.label_title: Optional[ttk.Label]=None
        self.parent = parent
        self.parent_row = 0
        self.parent_column = 0

        self.row = 0
        self.column = 0

        self.top = None
        self.canvas = None
        self.scroll_position = None

        if settings_knowledge_collections and items:
            is_changed = settings_knowledge_collections.fill_with(items)
            if is_changed:
                callback_settings(settings_knowledge_collections)

        self.build_ui()

    def lift(self):
        if self.top:
            if self.top.state() == 'iconic':
                self.top.deiconify()
            self.top.lift()
        else:
            self.build_ui()


    def on_list_key_changed(self, list_key: [str], enum_edit: Enum_Edit, i:int):
        self.list_key = list_key
        list_item = self.settings_knowledge_collections.get_list_item_by_list_key(list_key=list_key)
        self.callback(list_item)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.top = None

    def build_ui(self):

        if self.canvas:
            self.scroll_position = self.canvas.yview()
        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 400
        top_height = 400
        self.top.geometry(f"{top_width}x{top_height}")
        # self.top.attributes("-topmost", True)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + parent_width - top_width
        y = self.parent.winfo_y() + 50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = screen_width - top_width
        # 應用幾何位置
        self.top.geometry(f"{top_width}x{top_height}+{x}+{y}")

        self.canvas = tk.Canvas(self.top)
        scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=self.canvas.yview)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 配置 Canvas 的垂直滾動
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.root, anchor="nw")

        # 綁定 Frame 大小變化時更新滾動區域
        def update_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.root.bind("<Configure>", update_scrollregion)
        style = ttk.Style()
        style.configure("Narrow.TButton", width=2)

        self.row = 0
        self.label_title = ttk.Label(self.root, text=self.translator.get_translation("knowledge_collection_picker"),
                                     style="Config_Title.TLabel")
        self.label_title.grid(row=0, column=0, columnspan=4)
        self.row += 1
        List_Editor_Combo(self.root, var=self.list_key, callback=self.on_list_key_changed,
                          combo_source=self.settings_knowledge_collections.get_list_collection_name(),
                                is_separator=True).grid(row=self.row, column=0)


        if self.scroll_position:
            _scroll_to = self.scroll_position[0]
        else:
            _scroll_to = 1.0
        self.canvas.yview_moveto(_scroll_to)
        self.canvas.after(100, lambda: self.canvas.yview_moveto(_scroll_to))


class Editor_LLM_API(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable, translator: LanguageTranslator, llm_api: LLM_API,
                 settings_llms_api: Optional[LLMS_API] = None):
        super().__init__(parent=parent, callback=callback, translator=translator)
        # super().__init__()
        # self.parent = parent
        # self.callback = callback
        # self.translator = translator
        # self.root = None
        self.llm_api: LLM_API = llm_api

        self.llm_api_name_selected: Optional[str] = None
        self.settings_llms_api: LLMS_API = settings_llms_api

        self.label_title: Optional[ttk.Label] = None
        self.selector_settings_llms_api: Optional[Combo_Text_Editor] = None
        self.button_copy: Optional[ttk.Button] = None
        self.selector_llm_type: Optional[Combo_Text_Editor] = None
        self.editor_base_url: Optional[Text_Editor] = None
        self.editor_api_key: Optional[Text_Editor] = None
        self.editor_temperature: Optional[Text_Editor] = None
        self.editor_context_length: Optional[Text_Editor] = None
        self.editor_top_p: Optional[Text_Editor] = None
        self.editor_top_k: Optional[Text_Editor] = None
        self.editor_max_tokens: Optional[Text_Editor] = None
        #self.checkbox_is_stream: Optional[CheckBox_Editor] = None


    def on_enum_llm_changed(self, enum_value: str):
        self.llm_api.set_enum_llm( ENUM_LLM.from_value(enum_value))
      #  self.llm_api.set_base_url(self.llm_api.enum_llm.value.base_url)
        self.callback(self.llm_api)
        self.build_ui()

    def on_base_url_changed(self, base_url: str):
        self.llm_api.set_base_url(base_url)
        self.callback(self.llm_api)

    def on_api_access_key_changed(self, api_access_key: str):
        self.llm_api.set_api_access_key(api_access_key)
        self.callback(self.llm_api)

    def on_temperature_changed(self, temperature):
        _temp = temperature
        if isinstance(temperature, str):
            _temp = float(temperature)
        self.llm_api.set_temperature(_temp)
        self.callback(self.llm_api)

    def on_context_length_changed(self, context_length_str: str):
        self.llm_api.set_context_length(int(context_length_str))
        self.callback(self.llm_api)

    def on_top_p_changed(self, top_p_str: str):
        self.llm_api.set_top_p(float(top_p_str))
        self.callback(self.llm_api)

    def on_top_k_changed(self, top_k_str: str):
        self.llm_api.set_top_k(int(top_k_str))
        self.callback(self.llm_api)

    def on_max_tokens_changed(self, max_tokens_str: str):
        self.llm_api.set_max_tokens(int(max_tokens_str))
        self.callback(self.llm_api)

    #def on_timeout_changed(self, timeout_str: str):
    #    self.llm_api.set_timeout(float(timeout_str))
    #    self.callback(self.llm_api)

    #def on_is_stream_changed(self, is_stream: bool):
    #    self.llm_api.set_is_stream(bool(is_stream))
    #    self.callback(self.llm_api)

    def on_selector_settings_llms_api_changed(self, key: str):
        if key:
            self.llm_api_name_selected = key

    def on_button_copy_clicked(self):
        if self.llm_api_name_selected:
            self.llm_api = deepcopy(self.settings_llms_api.get_item(self.llm_api_name_selected))
            self.callback(self.llm_api)
            self.build_ui()


    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        row=0
       # self.label_title = ttk.Label(self.root, text="LLM API", style="Config_Title.TLabel")
       # self.label_title.grid(row=row, column=0)
       # self.llm_api.set_timeout(0)
       # row += 1
#
        if self.settings_llms_api and self.settings_llms_api.length()>0:
            self.selector_settings_llms_api = Combo_Text_Editor(self.root,
                                                                var="",
                                                                callback=self.on_selector_settings_llms_api_changed,
                                                                label=self.translator.get_translation(
                                                                    "llms_api_in_settings"),
                                                                combo_source=self.settings_llms_api.get_list_key(),
                                                               ).grid(
                row=row, column=0, field_width=40 )

            self.button_copy = ttk.Button(self.root, text=self.translator.get_translation("copy"),
                                          command=self.on_button_copy_clicked)
            self.button_copy.grid(row=row, column=1)
            self.llm_api_name_selected = self.settings_llms_api.get_list_key()[0]
            row += 1


        list_enum_llm_name = [member.value.name for member in ENUM_LLM]
        if not self.llm_api.enum_llm:
            self.on_enum_llm_changed(list_enum_llm_name[0])


        self.selector_llm_type = Combo_Text_Editor(self.root,
                                                   var=self.llm_api.enum_llm.value.name,
                                                   callback=self.on_enum_llm_changed,
                                                   label=self.translator.get_translation("llm_type"),
                                                   combo_source=list_enum_llm_name,
                                                   ).grid(row=row, column=0,  field_width=40)
        row += 1

        self.editor_base_url = Text_Editor(self.root, var=self.llm_api.base_url,callback=self.on_base_url_changed, label="Base URL",
                                           ).grid(row=row, column=0 , field_width=40  )
        row += 1

        self.editor_api_key = Text_Editor(self.root, var=self.llm_api.api_access_key, callback=self.on_api_access_key_changed, label="API Key",
                                          ).grid(row=row, column=0 , field_width=30   )
        row += 1
        Slider(self.root,var=self.llm_api.temperature, callback=self.on_temperature_changed,
               label="Temperature",
               legend1=self.translator.get_translation("accuracy"),
               legend2=self.translator.get_translation("creativity"), min_var=0.5, max_var=1.5, step=0.1,
               ).grid(row=row, column=0)

        row += 1

        self.editor_context_length = Text_Editor(self.root, var=str(self.llm_api.context_length),
                                                 callback=self.on_context_length_changed,
                                                 label="Context Length",).grid( row=row,  column=0)
        row += 1

        self.editor_top_p = Text_Editor(self.root, var=str(self.llm_api.top_p), callback=self.on_top_p_changed,
                                        label="Top P", ).grid(row=row, column=0)
        row += 1

        self.editor_top_k = Text_Editor(self.root, var=str(self.llm_api.top_k),callback=self.on_top_k_changed,
                                        label="Top K",    ).grid(row=row, column=0)
        row += 1

        self.editor_max_tokens = Text_Editor(self.root, var=str(self.llm_api.max_tokens),callback=self.on_max_tokens_changed,
                                             label="Max Tokens",   ).grid(row=row, column=0)
        row += 1

        #self.checkbox_is_stream = CheckBox_Editor(self.root, label="Stream", value=self.llm_api.is_stream,
        #                                          callback=self.on_is_stream_changed).grid(
        #    row=10, column=0)

       # Text_Editor(self.root, text=str(self.llm_api.timeout), label=self.translator.get_translation("timeout_limit"),
       #                                      callback=self.on_timeout_changed).grid(row=10,column=0)

class Editor_LLMS_API(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable,
                 translator: Optional[LanguageTranslator]=None,
                 callback_settings:Optional[Callable]=None,
                 llms_api: Optional[LLMS_API] = None, settings_llms_api: Optional[LLMS_API] = None):
        super().__init__(parent=parent, callback=callback, translator=translator)
        #super().__init__()
        #self.callback = callback
        #self.translator = translator
        #self.parent = parent
        #self.root: Optional[TK_WINDOW] = None

        self.new_llms_api : LLMS_API = llms_api if llms_api else LLMS_API()
        self.settings_llms_api = settings_llms_api
        self.list_new_llm_api: List[LLM_API] = self.new_llms_api.get_list_item()
        self.list_new_key = [item.key for item in self.list_new_llm_api]
        self.list_is_expanded: List[bool] = [False] * len(self.list_new_key) if len(self.list_new_key) > 0 else []
        self.label_title: Optional[ttk.Label]=None
        self.list_button_minus: List[ttk.Button] = []
        self.list_button_plus: List[ttk.Button] = []
        self.list_button_expand_collapse: List[ttk.Button] = []
        self.list_editor: List[Editor_LLM_API] = []

        self.parent_row = 0
        self.parent_column = 0

        self.row = 0
        self.column = 0

        self.top = None

        if settings_llms_api and llms_api and callback_settings:
            is_changed = settings_llms_api.fill_with(llms_api)
            if is_changed:
                callback_settings(settings_llms_api)

        self.build_ui()

    def lift(self):
        if self.top:
            if self.top.state() == 'iconic':
                self.top.deiconify()
            self.top.lift()
        else:
            self.build_ui()

    def geometry(self, geometry_str:str):
        self.top.geometry(geometry_str)

    def get_window_origin_x(self):
        return self.top.winfo_x()

    def get_window_origin_y(self):
        return self.top.winfo_y()

    def get_width(self):
        return self.top.winfo_width()

    def get_height(self):
        return self.top.winfo_height()

    def on_llm_api_changed(self, new_llm_api: LLM_API, i):
        #new_variable = self.list_editor[i].variable
        self.list_new_key[i] = new_llm_api.key
        self.list_new_llm_api[i] = new_llm_api
        self.new_llms_api.set_list_item(self.list_new_llm_api)
        self.callback(self.new_llms_api)

    def click_minus(self, index: int):
        if 0 <= index < len(self.list_new_key):
            self.list_new_llm_api.pop(index)
            self.list_new_key.pop(index)
            self.list_is_expanded.pop(index)
            self.new_llms_api.set_list_item(self.list_new_llm_api)

            self.build_ui()
            self.callback(self.new_llms_api)

    def click_plus(self, i: int):
        if 0 <= i <= self.new_llms_api.length():
            enum_llm = ENUM_LLM.GPT_3_5_TURBO
            item = self.new_llms_api.get_new_item(enum_llm=enum_llm)
            if i < self.new_llms_api.length():
                self.list_new_llm_api.insert(i, item)
                self.list_new_key.insert(i, enum_llm.value.name)
                self.list_is_expanded.insert(i, False)
            else:
                self.list_new_llm_api.append(item)
                self.list_new_key.append(enum_llm.value.name)
                self.list_is_expanded.append(False)
            self.new_llms_api.set_list_item(self.list_new_llm_api)
            self.build_ui()

            self.callback(self.new_llms_api)

    def click_expand_collapse(self, i: int):
        self.list_is_expanded[i] = not self.list_is_expanded[i]
        self.build_ui()

    def count_expand(self) -> int:
        count = 0
        for is_expand in self.list_is_expanded:
            if is_expand:
                count += 1
        return count

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.top = None

    def build_ui(self):
        size_of_list = len(self.list_new_key)
        #delta_rows = 0
        #delta_cols = 1 if self.count_expand() > 0 else 0
        delta_cols = 0
        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 600
        top_height = 400
        self.top.geometry(f"{top_width}x{top_height}")
        #self.top.attributes("-topmost", True)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + parent_width - top_width
        y = self.parent.winfo_y() +50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = screen_width - top_width
        # 應用幾何位置
        self.top.geometry(f"{top_width}x{top_height}+{x}+{y}")

        canvas = tk.Canvas(self.top)
        scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=canvas.yview)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 配置 Canvas 的垂直滾動
        canvas.configure(yscrollcommand=scrollbar.set)

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.root, anchor="nw")

        # 綁定 Frame 大小變化時更新滾動區域
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.root.bind("<Configure>", update_scrollregion)
        style = ttk.Style()
        style.configure("Narrow.TButton", width=2)
        self.row = 0
        self.label_title = ttk.Label(self.root, text=self.translator.get_translation("llm_api_editor"), style="Config_Title.TLabel")
        self.label_title.grid(row=0, column=0, columnspan=4)
        self.row += 1
        for i in range(0, size_of_list + 1):
            button_plus = ttk.Button(self.root, style="Narrow.TButton", text="+", command=lambda idx=i: self.click_plus(idx))
            button_plus.grid(row=self.row + 2*i , column=self.column + 1, padx=1)
            self.list_button_plus.append(button_plus)

            if i < size_of_list:
                button_minus = ttk.Button(self.root, style="Narrow.TButton", text="-", command=lambda idx=i: self.click_minus(idx))
                button_minus.grid(row=self.row + 2*i , column=self.column, padx=1)
                self.list_button_minus.append(button_minus)
                if self.list_is_expanded[i]:
                    button_text = "<"
                else:
                    button_text = ">"
                button = ttk.Button(self.root, width=2, text=button_text,
                                    command=lambda idx=i: self.click_expand_collapse(idx))
                button.grid(row=self.row + 2 * i, column=self.column + 2 + delta_cols, padx=1)
                self.list_button_expand_collapse.append(button)

                editor = None
                if self.list_is_expanded[i]:
                    editor = Editor_LLM_API(self.root, llm_api=self.new_llms_api.get_item(self.list_new_key[i]), settings_llms_api=self.settings_llms_api,
                                              callback=lambda llm_api, current_i=i: self.on_llm_api_changed(llm_api,current_i), translator=self.translator)
                    editor.grid(row=self.row + 2*i , column=self.column + 3, sticky="w")
                else:
                    editor = ttk.Label(self.root, text=self.new_llms_api.get_item(self.list_new_key[i]).key)
                    editor.grid(row=self.row + 2*i , column=self.column + 3, sticky="w")

                separator = ttk.Separator(self.root, orient="horizontal")
                separator.grid(row=self.row + 2 * i + 1, column=0, columnspan=4, sticky="ew", pady=5)
                #if self.list_is_expanded[i]:
                #    delta_rows += 2

                self.list_editor.append(editor)

        #self.root.update_idletasks()
        #parnet_width = self.parent.winfo_screenwidth()
        #parent_height = self.parent.winfo_screenheight()
        #width = self.root.winfo_screenwidth()
        #height = self.root.winfo_screenheight()
        #x = int( (parnet_width - width) / 2)
        #y = int( (parent_height - height) / 2)
        #self.root.geometry(f"{width}x{height}+{x}+{y}")


#lass Configer_SCHEDULE_TIME(Node_Configer_Base):
#   def __init__(self, parent: TK_WINDOW, callback: Callable, translator: LanguageTranslator,schedule_time: Optional[SCHEDULE_TIME] = None):
#       super().__init__( parent=parent, callback=callback, translator=translator)
#       #super().__init__()
#       #self.parent = parent
#       #self.callback = callback
#       #self.translator = translator
#       #self.root = None

#       self.schedule_time: SCHEDULE_TIME = schedule_time if schedule_time else SCHEDULE_TIME()
#       self.row = None
#       self.column = None
#       self.columnspan = None
#       self.padx = None
#       self.pady = None
#       self.sticky = None


#       self.top = None
#       self.is_pack=True

#       self.build_ui()

#   def lift(self):
#       if self.top:
#           if self.top.state() == 'iconic':
#               self.top.deiconify()
#           self.top.lift()
#       else:
#           self.build_ui()

#   def on_enum_timely_repeat_changed(self, enum_value: str):
#       self.schedule_time.set_enum_repeat_type(get_enum_by_value_TIMELY_REPEAT(enum_value))
#       self.callback(self.schedule_time)

#   def on_time_start_changed(self, time_start: datetime):
#       self.schedule_time.set_time_start(time_start)
#       self.callback(self.schedule_time)

#   def on_time_interval_changed(self, time_interval: DATE_TIME_PART):
#       self.schedule_time.set_time_interval(time_interval)
#       self.callback(self.schedule_time)

#   def on_time_assigned_changed(self, list_time_assigned: List[DATE_TIME_PART], enum_edit: Enum_Edit, i: int):
#       time_assigned = DATE_TIME_PARTS()
#       time_assigned.from_list(list_time_assigned)
#       self.schedule_time.set_time_assigned( time_assigned)
#       self.callback(self.schedule_time)

#   def on_first_call_implement_changed(self, is_first_call_implement: bool):
#       self.schedule_time.set_is_first_call_implement(is_first_call_implement)
#       self.callback(self.schedule_time)

#   def refresh(self):
#       self.build_ui()

#   def destroy(self):
#       destroy_TK_WINDOW(self.top)
#       self.top = None

#   def build_ui(self):
#       self.destroy()
#       self.top = tk.Toplevel(master=self.parent)
#       top_width = 500
#       top_height = 400
#       self.top.geometry(f"{top_width}x{top_height}")
#       #self.top.attributes("-topmost", True)
#       self.top.protocol("WM_DELETE_WINDOW", self.destroy)
#       self.parent.update_idletasks()
#       parent_x = self.parent.winfo_x()
#       parent_width = self.parent.winfo_width()
#       x = parent_x + parent_width - top_width
#       y = self.parent.winfo_y() + 50
#       screen_width = self.parent.winfo_screenwidth()
#       x = max(0, x)  # 避免 x 為負值
#       # 如果右側超出螢幕，則貼緊螢幕右邊界
#       if x + top_width > screen_width:
#           x = screen_width - top_width
#       # 應用幾何位置
#       self.top.geometry(f"{top_width}x{top_height}+{x}+{y}")

#       canvas = tk.Canvas(self.top)
#       scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=canvas.yview)

#       # 使用 grid 佈局排列 Canvas 和 Scrollbar
#       canvas.grid(row=0, column=0, sticky="nsew")
#       scrollbar.grid(row=0, column=1, sticky="ns")

#       # 配置 Canvas 的垂直滾動
#       canvas.configure(yscrollcommand=scrollbar.set)

#       # 讓 Canvas 隨窗口擴展
#       self.top.grid_rowconfigure(0, weight=1)
#       self.top.grid_columnconfigure(0, weight=1)

#       # 在 Canvas 中創建可滾動的 Frame
#       self.root = ttk.Frame(canvas)

#       canvas.create_window((0, 0), window=self.root, anchor="nw")

#       # 綁定 Frame 大小變化時更新滾動區域
#       def update_scrollregion(event):
#           canvas.configure(scrollregion=canvas.bbox("all"))

#       self.root.bind("<Configure>", update_scrollregion)

#       ttk.Label(self.root, text=self.translator.get_translation("project_schedule"), style="Config_Title.TLabel").grid(row=0, column=0)

#       list_timely_repeat_value = [member.value for member in ENUM_TIMELY_REPEAT]
#       if not self.schedule_time.enum_timely_repeat:
#           self.on_enum_timely_repeat_changed(list_timely_repeat_value[0])

#       Combo_Text_Editor(self.root, text=self.schedule_time.enum_timely_repeat.value,
#                               label=self.translator.get_translation("schedule_type"),
#                         combo_source=list_timely_repeat_value,
#                         callback=self.on_enum_timely_repeat_changed).grid(row=1, column=0, columnspan=10)
#       frame_start_time = ttk.Frame(self.root)
#       frame_start_time.grid(row=2, column=0, sticky="w")
#       ttk.Label(frame_start_time, text=self.translator.get_translation("start_time")).grid(row=0, column=0)
#       Date_Time_Editor(frame_start_time, date_time=self.schedule_time.time_start, callback=self.on_time_start_changed).grid( row=0,
#                        column=1, )
#       frame_time_interval = ttk.Frame(self.root)
#       frame_time_interval.grid(row=3, column=0, sticky="w")
#       ttk.Label(frame_time_interval, text=self.translator.get_translation("time_interval")).grid(row=0, column=0)
#       Time_Interval_Editor(frame_time_interval, time_interval=self.schedule_time.time_interval,
#                            callback=self.on_time_interval_changed).grid( row=0, column=1)

#       frame_time_assigned = ttk.Frame(self.root)
#       frame_time_assigned.grid(row=4, column=0, sticky="w")
#       ttk.Label(frame_time_assigned, text=self.translator.get_translation("time_assigned")).grid(row=0, column=0)
#       list_time_interval = self.schedule_time.time_assigned.to_list() if self.schedule_time.time_assigned else None
#       List_Time_Interval_Editor(frame_time_assigned, list_time_interval=list_time_interval,
#                                 callback=self.on_time_assigned_changed).grid( row=0, column=1)
#       CheckBox_Editor(self.root, value=self.schedule_time.is_first_call_implement, label=self.translator.get_translation("first_call_implement"),
#                               callback=self.on_first_call_implement_changed).grid( row=5, column=0)

class Editor_VARIABLE(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable,  translator: LanguageTranslator,variable: VARIABLE):
        super().__init__( parent=parent, callback=callback, translator=translator)
   #    super().__init__()
   #    self.parent = parent
   #    self.callback = callback
   #    self.root = None

        self.variable = variable
        self.row = 0
        self.column = 0


   #def grid(self, row: int = 0, column: int = 0, columnspan: int = 1, padx: int = 1, pady: int = 1,
   #         sticky: str = "w") -> "Editor_VARIABLE":

   #    self.root = tk.Frame(self.parent)
   #    self.root.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
   #    self.build_ui()
   #    return self

   #def destroy(self):
   #    destroy_TK_WINDOW(self.root)

    def on_enum_variable_changed(self, enum_variable_str: str):
        if self.variable.enum_variable.value != enum_variable_str:
            self.variable.enum_variable = ENUM_VARIABLE.from_value(enum_variable_str)
            self.variable.init_default_value()
            self.callback(self.variable)
            destroy_TK_WINDOW(self.root, is_destroy_root=False)
            self.build_ui()

    def on_name_changed(self, name: str):
        self.variable.set_name(name)
        self.callback(self.variable)

    def on_value_changed(self, value_srt: str):
        self.variable.set_default_value_from_str(value_srt)
        self.callback(self.variable)

    def on_list_changed(self, list_value: [], enum_edit, i):
        self.variable.set_default_value(list_value)
        self.callback(self.variable)

    def on_dict_changed(self, dict_text: {}, enum_edit, i):
        self.variable.set_default_value(dict_text)
        self.callback(self.variable)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        Text_Editor(self.root, var=self.variable.name,  callback=self.on_name_changed,label=self.translator.get_translation("name"),).grid(
                    row=self.row, column=self.column, field_width=30)
        Combo_Text_Editor(self.root, var=self.variable.enum_variable.value,
                          callback=self.on_enum_variable_changed,
                                label=self.translator.get_translation("variable_type"),
                                combo_source=[member.value for member in ENUM_VARIABLE],
                                ).grid( row=self.row+1, column=self.column  )
        match self.variable.enum_variable:
            case ENUM_VARIABLE.STRING | ENUM_VARIABLE.INT | ENUM_VARIABLE.FLOAT:
                Text_Editor(self.root, var=self.variable.get_value_str(),callback=self.on_value_changed,
                                  label=self.translator.get_translation("default_value"), ).grid(
                    row=self.row + 2,     column=self.column, field_width=20)
            case ENUM_VARIABLE.LIST:
                ttk.Label(self.root, text=self.translator.get_translation("default_value")).grid(row=self.row + 2, column=self.column, sticky="w")

                List_Editor_Text(self.root, var=self.variable.default_value, callback=self.on_list_changed).grid(
            row=self.row + 3,            column=self.column, field_width=20)

            case ENUM_VARIABLE.DICT:
                ttk.Label(self.root, text=self.translator.get_translation("key_value")).grid(row=self.row + 2,
                                                                                       column=self.column,
                                                                                       sticky="ew")

                List_Editor_Dict(self.root, var=self.variable.default_value, callback=self.on_dict_changed).grid(
                    row=self.row + 3,                    column=self.column,
                width_key=15, width_value=15)

class Editor_VARIABLES(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable, translator: LanguageTranslator, variables: Optional[VARIABLES] = None):
        super().__init__(parent=parent, callback=callback, translator=translator)
        #super().__init__()
        #self.parent = parent
        #self.callback = callback
        #self.root = None

        self.new_variables = variables if variables else []
        self.list_new_variable: List[VARIABLE] = self.new_variables.get_list_variable()
        self.list_new_key = [var.key for var in self.list_new_variable]
        self.list_is_expanded: List[bool] = [False] * len(self.list_new_key) if len(self.list_new_key) > 0 else []

        self.list_button_minus: List[ttk.Button] = []
        self.list_button_plus: List[ttk.Button] = []
        self.list_button_expand_collapse: List[ttk.Button] = []
        self.list_editor: List[Editor_VARIABLE] = []

        self.parent_row = 0
        self.parent_column = 0

        self.row = 0
        self.column = 0

        self.top = None
        self.canvas = None
        self.scroll_position=None
        self.build_ui()
   #def grid(self, row: int = 0, column: int = 0, columnspan: int = 1, padx: int = 1, pady: int = 1,
   #         sticky: str = "w") -> "Editor_VARIABLES":

   #    self.parent_row = row
   #    self.parent_column = column
   #    self.parent_sticky = sticky

   #    self.row = 0
   #    self.column = 0
   #    self.columnspan = columnspan
   #    self.root = None
   #
   #    return self

    def lift(self):
        if self.top:
            if self.top.state() == 'iconic':
                self.top.deiconify()
            self.top.lift()
        else:
            self.build_ui()
    def set_variables(self, variables: VARIABLES):
        self.new_variables = variables if variables else []
        self.list_new_variable: List[VARIABLE] = self.new_variables.get_list_variable()
        self.list_new_key = [var.key for var in self.list_new_variable]
        self.list_is_expanded: List[bool] = [False] * len(self.list_new_key) if len(self.list_new_key) > 0 else []
        self.destroy()
        self.build_ui()

    def on_variable_changed(self, new_variable: VARIABLE, i):
        #new_variable = self.list_editor[i].variable
        self.list_new_key[i] = new_variable.key
        self.list_new_variable[i] = new_variable
        self.new_variables.set_dict_with_list(self.list_new_variable)
        self.callback(self.new_variables)

    def click_minus(self, index: int):
        if 0 <= index < len(self.list_new_key):
            self.list_new_variable.pop(index)
            self.list_new_key.pop(index)
            self.list_is_expanded.pop(index)
            self.new_variables.set_dict_with_list(self.list_new_variable)

            self.build_ui()
            self.callback(self.new_variables)

    def click_plus(self, i: int):
        if 0 <= i <= self.new_variables.length():
            name = "var"
            var = VARIABLE(name=name, enum_variable=ENUM_VARIABLE.STRING)
            if i < self.new_variables.length():
                self.list_new_variable.insert(i, var)
                self.list_new_key.insert(i, name)
                self.list_is_expanded.insert(i, False)
            else:
                self.list_new_variable.append(var)
                self.list_new_key.append(name)
                self.list_is_expanded.append(False)
            self.new_variables.set_dict_with_list(self.list_new_variable)
            self.build_ui()

            self.callback(self.new_variables)

    def click_expand_collapse(self, i: int):
        self.list_is_expanded[i] = not self.list_is_expanded[i]
        self.build_ui()

    #def count_expand(self) -> int:
    #    count = 0
    #    for is_expand in self.list_is_expanded:
    #        if is_expand:
    #            count += 1
    #    return count

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.canvas = None
        self.top = None

    def build_ui(self):
        size_of_list = len(self.list_new_key)
        if self.canvas and self.canvas.winfo_exists():  # 检查组件是否有效
            self.scroll_position = self.canvas.yview()
        else:
            self.scroll_position = None

        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 600
        top_height = 400
        self.top.geometry(f"{top_width}x{top_height}")
        #self.top.attributes("-topmost", True)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + (parent_width - top_width)/2
        y = self.parent.winfo_y() + 50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = (screen_width - top_width)/2
        # 應用幾何位置
        geometry_str = f"{top_width}x{top_height}+{x}+{y}"
        self.top.geometry(f"{top_width}x{top_height}+{int(x)}+{int(y)}")
        self.canvas = tk.Canvas(self.top)
        scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=self.canvas.yview)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 配置 Canvas 的垂直滾動
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.root, anchor="nw")

        def update_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.root.bind("<Configure>", update_scrollregion)
        style = ttk.Style()
        style.configure("Narrow.TButton", width=2)

        self.row = 0
        self.label_title = ttk.Label(self.root, text=self.translator.get_translation("variable_editor"), style="Config_Title.TLabel")
        self.label_title.grid(row=0, column=0, columnspan=4)
        self.row += 1
        for i in range(0, size_of_list + 1):
            button_plus = ttk.Button(self.root, width=2, text="+", command=lambda idx=i: self.click_plus(idx))
            button_plus.grid(row=self.row + 2*i , column=self.column + 1, padx=1)
            self.list_button_plus.append(button_plus)

            if i < size_of_list:
                button_minus = ttk.Button(self.root, width=2, text="-", command=lambda idx=i: self.click_minus(idx))
                button_minus.grid(row=self.row + 2*i, column=self.column, padx=1)
                self.list_button_minus.append(button_minus)
                if self.list_is_expanded[i]:
                    button_text = "<"
                else:
                    button_text = ">"
                button = ttk.Button(self.root, width=2, text=button_text,
                                    command=lambda idx=i: self.click_expand_collapse(idx))
                button.grid(row=self.row + 2 * i, column=self.column + 2, padx=1)
                self.list_button_expand_collapse.append(button)

                if self.list_is_expanded[i]:
                    editor = Editor_VARIABLE(self.root, variable=self.new_variables.get_variable(self.list_new_key[i]),
                                             callback=lambda variable, current_i=i: self.on_variable_changed(variable,
                                                                                                             current_i),
                                             translator=self.translator)

                    editor.grid(row=self.row + 2*i, column=self.column + 3, sticky="w")

                else:
                    editor = ttk.Label(self.root, text=self.new_variables.get_variable(self.list_new_key[i]).key)
                    editor.grid(row=self.row + 2*i , column=self.column + 3, sticky="w")


                separator = ttk.Separator(self.root, orient="horizontal")
                separator.grid(row=self.row + 2 * i + 1, column=0, columnspan=4, sticky="ew", pady=5)
                #if self.list_is_expanded[i]:
                #    delta_rows += 2

                self.list_editor.append(editor)
        if self.scroll_position:
            _scroll_to = self.scroll_position[0]
        else:
            _scroll_to = 1.0
        self.canvas.yview_moveto(_scroll_to)
        self.canvas.after(100, lambda: self.canvas.yview_moveto(_scroll_to))

class Viewer_VARIABLES(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, translator: LanguageTranslator, variables: Optional[VARIABLES] = None):
        super().__init__(parent=parent, callback=None, translator=translator)

        self.variables = variables
        self.parent_row = 0
        self.parent_column = 0

        self.row = 0
        self.column = 0

        self.top = None
        self.build_ui()

    def lift(self):
        if self.top:
            if self.top.state() == 'iconic':
                self.top.deiconify()
            self.top.lift()
        else:
            self.build_ui()

    def set_variables(self, variables: VARIABLES):
        self.variables = variables
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.top = None

    def refresh(self):
        self.build_ui()

    def build_ui(self):

        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 550
        top_height = 400
        self.top.geometry(f"{top_width}x{top_height}")
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + (parent_width - top_width)/2
        y = self.parent.winfo_y() + 50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = (screen_width - top_width)/2
        # 應用幾何位置
        geometry_str = f"{top_width}x{top_height}+{x}+{y}"
        self.top.geometry(f"{top_width}x{top_height}+{int(x)}+{int(y)}")
        canvas = tk.Canvas(self.top)
        scrollbar = ttk.Scrollbar(self.top, orient="vertical", command=canvas.yview)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 配置 Canvas 的垂直滾動
        canvas.configure(yscrollcommand=scrollbar.set)

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.root, anchor="nw")

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.root.bind("<Configure>", update_scrollregion)
        style = ttk.Style()
        style.configure("Narrow.TButton", width=2)

        self.row = 0
        label_title = ttk.Label(self.root, text=self.translator.get_translation("variables_viewer"), style="Config_Title.TLabel")
        label_title.grid(row=0, column=0, columnspan=4)
        self.row += 1
        ttk.Label(self.root, text=self.translator.get_translation("key")).grid(row=self.row , column=0, sticky="w")
        ttk.Label(self.root, text=' | ').grid(row=self.row, column=1, sticky="w")
        ttk.Label(self.root, text=self.translator.get_translation("value")).grid(row=self.row, column=2, sticky="w")
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.grid(row=self.row + 1, column=0, columnspan=3, sticky="ew", pady=5)
        self.row += 2
        i=0
        for variable in self.variables.dict_variable.values():
            ttk.Label(self.root, text=variable.key).grid(row=self.row+i, column=0, sticky="w")
            ttk.Label(self.root, text=' | ').grid(row=self.row + i, column=1, sticky="w")
            ttk.Label(self.root, text=variable.get_value_str()).grid(row=self.row + i, column=2, sticky="w")
            separator = ttk.Separator(self.root, orient="horizontal")
            separator.grid(row=self.row + i + 1, column=0, columnspan=3, sticky="ew", pady=5)
            i+=2

class Editor_LINE(Node_Configer_Base):
    def __init__(self, parent: TK_WINDOW, callback: Callable, label: str, value:str,  translator: LanguageTranslator):
        super().__init__( parent=parent, callback=callback, translator=translator)

        self.label = label
        self.value = value
        self.row = 0
        self.column = 0
        self.top = None
        self.build_ui()

    def on_value_changed(self, value: str):
        self.value = value
        self.callback(self.value)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.top)
        self.top = None

    def build_ui(self):
        self.destroy()
        self.top = tk.Toplevel(master=self.parent)
        top_width = 400
        top_height = 100
        self.top.geometry(f"{top_width}x{top_height}")
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_width = self.parent.winfo_width()
        x = parent_x + (parent_width - top_width) / 2
        y = self.parent.winfo_y() + 50
        screen_width = self.parent.winfo_screenwidth()
        x = max(0, x)  # 避免 x 為負值
        # 如果右側超出螢幕，則貼緊螢幕右邊界
        if x + top_width > screen_width:
            x = (screen_width - top_width) / 2
        # 應用幾何位置
        geometry_str = f"{top_width}x{top_height}+{x}+{y}"
        self.top.geometry(f"{top_width}x{top_height}+{int(x)}+{int(y)}")
        canvas = tk.Canvas(self.top)

        # 使用 grid 佈局排列 Canvas 和 Scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")

        # 讓 Canvas 隨窗口擴展
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        # 在 Canvas 中創建可滾動的 Frame
        self.root = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.root, anchor="nw")

        Text_Editor(self.root, var=self.value,  callback=self.on_value_changed, label=self.translator.get_translation(self.label)).grid(
                    row=self.row, column=self.column, field_width=30)


class Configer_NODE_CRAWL(Node_Configer_Base):
    def __init__(self, node: NODE_CRAWL, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.root = ttk.Frame(self.parent)
        self.row = 0
        self.column = 0

    def on_keywords_changed(self, keywords: List):
        self.node.set_keywords(keywords)
        self.callback(self.node)

    def on_search_engine_changed(self, search_engine: str):
        self.node.set_search_engine(search_engine)
        self.callback(self.node)

    def on_api_keys_dict_changed(self, api_keys_dict: Dict):
        self.node.set_api_keys_dict(api_keys_dict)
        self.callback(self.node)

    def on_limit_web_pages_changed(self, limit_str: str):
        self.node.set_limit_web_pages(int(limit_str))
        self.callback(self.node)

    def on_limit_layers_changed(self, limit_str: str):
        self.node.set_limit_layers(int(limit_str))
        self.callback(self.node)

    def on_timeout_changed(self, timeout_str: str):
        if timeout_str or len(timeout_str)>0:
            timeout = int(timeout_str)
        else:
            timeout = 0
        if timeout > 0:
            self.node.set_timeout(timeout)
            self.callback(self.node)
        else:
            messagebox.showwarning("警告", "必須為正整數！")

    def on_buffer_size_changed(self, buffer_size_str: str):
        buffer_size = int(buffer_size_str)
        if buffer_size > 0:
            self.node.set_buffer_size(buffer_size)
            self.callback(self.node)
        else:
            messagebox.showwarning("警告", "必須為正整數！")

    def on_crawled_data_primary_name_changed(self, crawled_data_primary_name: str):
        self.node.set_crawled_data_primary_name(crawled_data_primary_name)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        self.row = 0
        ttk.Label(self.root, text=self.translator.get_translation("keywords")).grid(row=self.row, column=0, sticky="w")
        self.row += 1
        List_Editor_Text(self.root, var=self.node.keywords, callback=self.on_keywords_changed,).grid( row=self.row, column=0)
        self.row +=1
        Combo_Text_Editor(self.root, var=str(self.node.search_engine), callback=self.on_search_engine_changed,
                    label=self.translator.get_translation("search_engine"), combo_source= self.node.search_engines ).grid(row=self.row, column=0)
        self.row += 1
        ttk.Label(self.root, text=self.translator.get_translation("api_keys")).grid(row=self.row, column=0, sticky="w")
        self.row += 1
        List_Editor_Dict(self.root, var=self.node.api_keys_dict, callback=self.on_api_keys_dict_changed).grid(row=self.row, column=0)
        self.row += 1
        Text_Editor(self.root, var=str(self.node.limit_web_pages), callback=self.on_limit_web_pages_changed,
                    label=self.translator.get_translation("limit_web_pages"),
                    ).grid(row=self.row, column=0)
        self.row += 1
        Text_Editor(self.root, var=str(self.node.limit_layers), callback=self.on_limit_layers_changed,
                    label=self.translator.get_translation("limit_layers"),
                    ).grid(row=self.row, column=0)
        self.row += 1
        Text_Editor(self.root, var=str(self.node.timeout),callback=self.on_timeout_changed,
                    label=self.translator.get_translation("timeout"),
                    ).grid( row=self.row, column=0)

class Configer_NODE_EXTRACT_TEXT(Node_Configer_Base):
    def __init__(self, node: NODE_EXTRACT_TEXT, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.root = ttk.Frame(self.parent)
        self.row = 0
        self.column = 0

    def on_filepath_changed(self, filepath: str, source: Enum_Text_Source):
        self.node.set_filepath_text_source(source)
        match source:
            case Enum_Text_Source.COMBO:
                self.node.set_filepath_variable_key(filepath)
            case Enum_Text_Source.TEXT_EDITOR | Enum_Text_Source.SCROLL_TEXT_EDITOR | Enum_Text_Source.FILEPATH_SELECTOR:
                self.node.set_filepath(filepath)
        self.callback(self.node)


    def on_output_variable_key_changed(self, key: str):
        self.node.set_output_variables_key([key])
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        self.row = 0
        ttk.Label(self.root, text=self.translator.get_translation("filepath")).grid(row=self.row, column=0, sticky="w")
        self.row += 1

        source_list = [
            (Enum_Text_Source.COMBO, "V"),
            (Enum_Text_Source.TEXT_EDITOR, "C"),
            # (Enum_Text_Source.FILEPATH_SELECTOR, "F")
        ]
        Composite_Text_Sourcer(self.root, var=str(self.node.filepath),
                               callback=self.on_filepath_changed,
                               label=self.translator.get_translation("filepath"),
                               enum_text_source=self.node.filepath_text_source,
                               list_text_source=source_list,
                               combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=self.row, column=0, switch_width=40)

        self.row +=1
        output_variable_key = ""
        if len(self.node.output_variables_key)>0:
            output_variable_key = self.node.output_variables_key[0]
        Combo_Text_Editor(self.root, var=output_variable_key, callback=self.on_output_variable_key_changed,
                    label=self.translator.get_translation("output_variable"), combo_source= self.node.global_variables.get_list_key() ).grid(row=self.row, column=0)
        self.row += 1



class Configer_NODE_SEND_MAIL(Node_Configer_Base):
    def __init__(self, node: NODE_SEND_MAIL, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_SEND_MAIL, node)

    def on_sender_email_variable_key_changed(self, variable_key: str):
        self.node.set_sender_email_variable_key(variable_key)
        self.callback(self.node)

    def on_password_variable_key_changed(self, password: str):
        self.node.set_password_variable_key(password)
        self.callback(self.node)

    def on_smtp_server_variable_key_changed(self, variable_key: str):
        self.node.set_smtp_server_variable_key(variable_key)
        self.callback(self.node)

    def on_smtp_port_variable_key_changed(self, variable_key: str):
        self.node.set_smtp_port_variable_key(variable_key)
        self.callback(self.node)

    def on_list_receivers_email_variable_key_changed(self, variable_key: str):
        self.node.set_list_receivers_email_variable_key(variable_key)
        self.callback(self.node)

    def on_subject_variable_key_changed(self, variable_key: str):
        self.node.set_subject_variable_key(variable_key)
        self.callback(self.node)

    def on_body_variable_key_changed(self, variable_key: str):
        self.node.set_body_variable_key(variable_key)
        self.callback(self.node)

    def on_list_attachment_variable_key_changed(self, variable_key: str):
        self.node.set_list_attachment_variable_key(variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        if not is_string_valid(self.node.sender_email_variable_key):
            self.on_sender_email_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root, var=self.node.sender_email_variable_key,
                          callback=self.on_sender_email_variable_key_changed,
                          label=self.translator.get_translation("sender_email_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                          ).grid(row=1, column=0, sticky="e")

        if not is_string_valid(self.node.password_variable_key):
            self.on_password_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root,  var=self.node.password_variable_key,
                          callback=self.on_password_variable_key_changed,
                          label=self.translator.get_translation("password_variable_key"),
                          combo_source=self.node.global_variables.get_list_key(),
                            ).grid( row=2, column=0, sticky="e")

        if not is_string_valid(self.node.smtp_server_variable_key):
            self.on_smtp_server_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root, var=self.node.smtp_server_variable_key,
                          callback=self.on_smtp_server_variable_key_changed,
                          label=self.translator.get_translation("smtp_server_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=3, column=0, sticky="e")

        if not is_string_valid(self.node.smtp_port_variable_key):
            self.on_smtp_port_variable_key_changed(self.node.global_variables.get_list_key()[0])
        Combo_Text_Editor(self.root,     var=self.node.smtp_port_variable_key,
                          callback=self.on_smtp_port_variable_key_changed,
                          label=self.translator.get_translation("smtp_port_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=4, column=0, sticky="e")

        if not is_string_valid(self.node.list_receivers_email_variable_key):
            self.on_list_receivers_email_variable_key_changed(self.node.global_variables.get_list_key()[0])
        Combo_Text_Editor(self.root,   var=self.node.list_receivers_email_variable_key,
                          callback=self.on_list_receivers_email_variable_key_changed,
                          label=self.translator.get_translation("list_receivers_email_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=5, column=0, sticky="e")

        if not is_string_valid(self.node.subject_variable_key):
            self.on_subject_variable_key_changed(self.node.global_variables.get_list_key()[0])
        Combo_Text_Editor(self.root,     var=self.node.subject_variable_key,
                          callback=self.on_subject_variable_key_changed,
                          label=self.translator.get_translation("subject_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                              ).grid(row=6, column=0, sticky="e")

        if not is_string_valid(self.node.body_variable_key):
            self.on_body_variable_key_changed(self.node.global_variables.get_list_key()[0])
        Combo_Text_Editor(self.root, label=self.translator.get_translation("body_variable_key"),
                                var=self.node.body_variable_key,
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_body_variable_key_changed).grid(row=7, column=0, sticky="e")

        if not is_string_valid(self.node.list_attachment_variable_key):
            self.on_list_attachment_variable_key_changed(self.node.global_variables.get_list_key()[0])
        Combo_Text_Editor(self.root,  var=self.node.list_attachment_variable_key,
                          callback=self.on_list_attachment_variable_key_changed,
                          label=self.translator.get_translation("list_attachment_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                              ).grid(row=8, column=0, sticky="e")

class Configer_NODE_RECEIVE_MAIL(Node_Configer_Base):
    def __init__(self, node: NODE_RECEIVE_MAIL, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_RECEIVE_MAIL, node)

    def on_email_addr_variable_key_changed(self, variable_key: str):
        self.node.set_email_addr_variable_key(variable_key)
        self.callback(self.node)

    def on_password_variable_key_changed(self, password: str):
        self.node.set_password_variable_key(password)
        self.callback(self.node)

    def on_imap_server_variable_key_changed(self, variable_key: str):
        self.node.set_imap_server_variable_key(variable_key)
        self.callback(self.node)

    def on_imap_port_variable_key_changed(self, variable_key: str):
        self.node.set_imap_port_variable_key(variable_key)
        self.callback(self.node)

    def on_enum_action_changed(self, enum_action_value: str):
        self.node.set_enum_action(ENUM_RECEIVE_MAIL_ACTION.from_value(enum_action_value))
        self.callback(self.node)
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        self.build_ui()

    def on_first_output_variable_key_changed(self, variable_key: str):
        if not self.node.output_variables_key:
            self.node.output_variables_key = []
        if len(self.node.output_variables_key) < 1:
            self.node.output_variables_key.append("")
        self.node.output_variables_key[0]=variable_key
        self.callback(self.node)

    def on_first_input_variable_key_changed(self, variable_key: str):
        if not self.node.input_variables_key:
            self.node.input_variables_key = []
        if len(self.node.input_variables_key)<1:
            self.node.input_variables_key.append("")
        self.node.input_variables_key[0]=variable_key
        self.callback(self.node)

    def on_second_input_variable_key_changed(self, variable_key: str):
        if not self.node.input_variables_key:
            self.node.input_variables_key = []
        if len(self.node.input_variables_key) < 1:
            self.node.input_variables_key.append("")
        if len(self.node.input_variables_key) < 2:
            self.node.input_variables_key.append("")
        self.node.input_variables_key[1] = variable_key
        self.callback(self.node)


    def refresh(self):
        self.build_ui()
    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        if not is_string_valid(self.node.email_addr_variable_key):
            self.on_email_addr_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root,   var=self.node.email_addr_variable_key,
                          callback=self.on_email_addr_variable_key_changed,
                          label=self.translator.get_translation("email_addr_variable_key"),
                               combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=1, column=0, sticky="e")

        if not is_string_valid(self.node.password_variable_key):
            self.on_password_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root,  var=self.node.password_variable_key,
                          callback=self.on_password_variable_key_changed,
                          label=self.translator.get_translation("password_variable_key"),
                                 combo_source=self.node.global_variables.get_list_key(),
                               ).grid( row=2, column=0, sticky="e")

        if not is_string_valid(self.node.imap_server_variable_key):
            self.on_imap_server_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root,   var=self.node.imap_server_variable_key,
                          callback=self.on_imap_server_variable_key_changed,
                          label=self.translator.get_translation("imap_server_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                              ).grid(row=3, column=0, sticky="e")

        if not is_string_valid(self.node.imap_port_variable_key):
            self.on_imap_port_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root,   var=self.node.imap_port_variable_key,
                          callback=self.on_imap_port_variable_key_changed,
                          label=self.translator.get_translation("imap_port_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=4, column=0, sticky="e")

        if not self.node.enum_action:
            self.on_enum_action_changed(ENUM_RECEIVE_MAIL_ACTION.ACTION_GET_MESSAGES_ID.value)
        Combo_Text_Editor(self.root,    var=self.node.enum_action.value,
                          callback=self.on_enum_action_changed,
                          label=self.translator.get_translation("action"),
                                combo_source=[member.value for member in ENUM_RECEIVE_MAIL_ACTION],
                               ).grid(row=5, column=0, sticky="e")

        if self.node.enum_action in [ENUM_RECEIVE_MAIL_ACTION.ACTION_PARSE_MAIL,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_SAVE_ATTACHMENTS,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_SET_MESSAGE_SEEN,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_DELETE_MESSAGE,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_SET_MESSAGES_SEEN,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_DELETE_MESSAGES,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_CREATE_FOLDER,
                                     ENUM_RECEIVE_MAIL_ACTION.ACTION_MOVE_MESSAGE]:
            ttk.Label(self.root, text=self.translator.get_translation("input_variables_key")).grid(row=6, column=0,
                                                                                                   sticky="w")
            if not self.node.input_variables_key or not is_string_valid(self.node.input_variables_key[0]):
                self.on_first_input_variable_key_changed(self.node.global_variables.get_list_key()[0])

        match self.node.enum_action:
            case ENUM_RECEIVE_MAIL_ACTION.ACTION_PARSE_MAIL | \
                 ENUM_RECEIVE_MAIL_ACTION.ACTION_SAVE_ATTACHMENTS | \
                 ENUM_RECEIVE_MAIL_ACTION.ACTION_SET_MESSAGE_SEEN | \
                 ENUM_RECEIVE_MAIL_ACTION.ACTION_DELETE_MESSAGE:
                    Combo_Text_Editor(self.root,  var=self.node.input_variables_key[0],
                                      callback=self.on_first_input_variable_key_changed,
                                      label=self.translator.get_translation("message_id_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                ).grid(row=7, column=0, sticky="e")

            case ENUM_RECEIVE_MAIL_ACTION.ACTION_SET_MESSAGES_SEEN | \
                 ENUM_RECEIVE_MAIL_ACTION.ACTION_DELETE_MESSAGES:
                Combo_Text_Editor(self.root,    var=self.node.input_variables_key[0],
                                  callback=self.on_first_input_variable_key_changed,
                                  label=self.translator.get_translation("messages_id_variable_key"),
                                        combo_source=self.node.global_variables.get_list_key(),
                                       ).grid(row=7, column=0,    sticky="e")
            case ENUM_RECEIVE_MAIL_ACTION.ACTION_CREATE_FOLDER:
                Combo_Text_Editor(self.root,    var=self.node.input_variables_key[0],
                                  callback=self.on_first_input_variable_key_changed,
                                  label=self.translator.get_translation("folder_name_variable_key"),
                                        combo_source=self.node.global_variables.get_list_key(),
                                       ).grid(row=7, column=0,  sticky="e")
            case    ENUM_RECEIVE_MAIL_ACTION.ACTION_MOVE_MESSAGE:
                    Combo_Text_Editor(self.root,  var=self.node.input_variables_key[0],
                                      callback=self.on_first_input_variable_key_changed,
                                      label=self.translator.get_translation("message_id_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=7, column=0, sticky="e")

                    if not self.node.input_variables_key or not is_string_valid(self.node.input_variables_key[1]):
                        self.on_second_input_variable_key_changed(self.node.global_variables.get_list_key()[0])
                    Combo_Text_Editor(self.root,  var=self.node.input_variables_key[1],
                                      callback=self.on_first_input_variable_key_changed,
                                      label=self.translator.get_translation("folder_name_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=8, column=0, sticky="e")

        label_output = ""

        match self.node.enum_action:
            case ENUM_RECEIVE_MAIL_ACTION.ACTION_GET_MESSAGES_ID:
                label_output="messages_id_variable_key"

            case ENUM_RECEIVE_MAIL_ACTION.ACTION_PARSE_MAIL:
                label_output ="message_info_variable_key"

            case ENUM_RECEIVE_MAIL_ACTION.ACTION_SAVE_ATTACHMENTS:
                label_output ="attachments_filepath_variable_key"

            case ENUM_RECEIVE_MAIL_ACTION.ACTION_GET_FOLDERS_NAME:
                label_output="folders_name_variable_key"

        if is_string_valid(label_output):
            if not self.node.output_variables_key or not is_string_valid(self.node.output_variables_key[0]):
                self.on_first_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

            ttk.Label(self.root, text=self.translator.get_translation("output_variable")).grid(row=9, column=0,
                                                                                                   sticky="w")
            Combo_Text_Editor(self.root,   var=self.node.output_variables_key[0],
                              callback=self.on_first_output_variable_key_changed,
                              label=self.translator.get_translation(label_output),
                                    combo_source=self.node.global_variables.get_list_key(),
                                  ).grid(row=10, column=0, sticky="e")

class Row_Editor_Header(Base_Row_Editor):
    """對應你提到的 Key: Value 結構"""
    def __init__(self, parent, var, callback, header_keys:Optional[Dict]=None, **kwargs):
        # value 預期為 (key, val)
        super().__init__(parent, var, callback, **kwargs)
        self.header_keys= header_keys
        self.combo_source= list(self.header_keys.keys())
        self.key_editor = None
        self.val_editor = None

    def _on_key_changed(self):
        v = self.header_keys[self.key_editor.value]
        self.var = {self.key_editor.value: v}
        self.val_editor.configure(var = v)
        self.callback(self.var)

    def _on_value_changed(self):
        self.var = {self.key_editor.value: self.val_editor.value }
        self.callback(self.var)

    def build_ui(self):
       # k, v = self.var if isinstance(self.var, dict) else next(iter(self.header_keys.items()))
        # 判斷當前這行應該顯示什麼
        k = ""
        v = ""

        if isinstance(self.var, dict) and self.var:
            # 如果 var 有資料，取出第一組 (這行通常只有一組 key-value)
            k = next(iter(self.var.keys()))
            v = self.var[k]
        else:
            # 如果是按 + 號剛產生的空行，預設選取 header_keys 的第一個
            k = next(iter(self.header_keys.keys()))
            v = self.header_keys[k]
            # 更新 self.var 確保資料同步
            self.var = {k: v}

        self.key_editor = Combo_Text_Editor(parent= self.root, var= k, callback= self._on_key_changed, combo_source= self.combo_source, **self.kwargs)
        self.key_editor.pack(side="left")

        ttk.Label(self.root, text=":").pack(side="left")
        self.val_editor = Text_Editor(self.root, v, self._on_value_changed, **self.kwargs)
        self.val_editor.pack(side="left")

class List_Editor_Headers(List_Editor):
    def __init__(self, parent: TK_WINDOW, var:Optional[List[str]]=None,  callback:Callable= None , **kwargs):
        # 1. 定義「最小必要」標頭 (預設會出現在畫面上的)
        default_header_keys_essential = {
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }

        # 2. 定義「常用但非必要」標頭 (只出現在下拉選單中)
        default_header_keys_common = {
            "Accept": "application/json",
            "User-Agent": "SmartPal/1.x",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Origin": "http://localhost",
            "Referer": "http://localhost",
            "Cookie": "",
            "X-Requested-With": "XMLHttpRequest"
        }

        # 3. 合併兩者，作為下拉選單的資料源 (combo_source)
        # 如果呼叫端沒傳入自定義的 header_keys，就用這組全集
        if 'header_keys' not in kwargs:
            # 使用字典合併語法 (Python 3.9+) 或 update
            all_keys = {**default_header_keys_essential, **default_header_keys_common}
            kwargs['header_keys'] = all_keys

        # 4. 如果 var 為空，使用 essential 內的項目來創建初始的 var
        # 我們將 essential 裡的每一對 key-value 都轉成一個獨立的 dict 放入 list
        if not var:
            var = []
            for k, v in default_header_keys_essential.items():
                var.append({k: v})

        super().__init__(parent=parent, var=var , callback=callback, row_class=Row_Editor_Header,  **kwargs)

class Configer_NODE_HTTP_REQUEST(Node_Configer_Base):
    def __init__(self, node: NODE_HTTP_REQUEST, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator,):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_HTTP_REQUEST, node)

    def on_url_str_changed(self, url_str: str):
        self.node.set_url_str(url_str)
        self.callback(self.node)

    def on_request_type_changed(self, request_type_value: str):
        self.node.set_request_type(get_http_request_type_enum_by_value(request_type_value))
        self.callback(self.node)

    def on_headers_changed(self, headers):
        #self.node.set_headers(json.loads(headers))
        self.node.set_headers(headers)
        self.callback(self.node)

    def on_body_data_changed(self, body_data_str: str):
        #self.node.set_body_data(json.loads(body_data_str))
        self.node.set_body_data_str(body_data_str)
        self.callback(self.node)

    def on_body_type_changed(self, body_type_str: str):
        self.node.set_body_type(RequestBodyType(body_type_str))
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str]= None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def on_timeout_changed(self, timeout_str: str):
        timeout = int(timeout_str)
        if timeout > 0:
            self.node.set_timeout(timeout)
            self.callback(self.node)
        else:
            messagebox.showwarning("警告", "必須為正整數！")

    def on_allow_redirects_changed(self, is_allow_redirects: bool):
        self.node.set_allow_redirects(is_allow_redirects)
        self.callback(self.node)

    def on_verify_ssl_changed(self, is_verify_ssl: bool):
        self.node.set_verify_ssl(is_verify_ssl)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()
    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        list_request_type_value = [member.value for member in ENUM_HTTP_REQUEST_TYPE]
        if not self.node.request_type:
            self.on_request_type_changed(list_request_type_value[0])

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Text_Editor(self.root, var=self.node.url_str, callback=self.on_url_str_changed, label="URL").grid( row=1, column=0, field_width=30)

        Combo_Text_Editor(self.root, var=self.node.request_type.value,
                          callback=self.on_request_type_changed,
                                label=self.translator.get_translation("request_type"),
                          combo_source=list_request_type_value,
                          ).grid( row=2, column=0,)

        ttk.Label(self.root, text=self.translator.get_translation("headers")).grid(row=3, column=0, sticky="w")
        #Scroll_Text_Editor(self.root, text=json.dumps(self.node.headers), callback=self.on_headers_changed).grid( row=4,
        #                   column=0, height=10)
        #Scroll_Text_Editor(self.root, var=self.node.headers_str, callback=self.on_headers_changed).grid(
        #    row=4,   column=0,    height=10)

        List_Editor_Headers(self.root, var=self.node.headers, callback=self.on_headers_changed, ).grid(
            row=4,   column=0)

        ttk.Label(self.root, text=self.translator.get_translation("body_data")).grid(row=5, column=0, sticky="w")
        #Scroll_Text_Editor(self.root, text=json.dumps(self.node.body_data), callback=self.on_body_data_changed).grid( row=6,
        #                   column=0, height=10)
        Scroll_Text_Editor(self.root, var=self.node.body_data_str, callback=self.on_body_data_changed).grid(
            row=6,   column=0, height=10)

        Combo_Text_Editor(self.root, var=self.node.body_type,
                          callback=self.on_body_type_changed,
                                label=self.translator.get_translation("body_type"),
                          combo_source= list(get_args(RequestBodyType)),
                         ).grid( row=7, column=0)
        output_variable_key = None
        if self.node.output_variables_key:
            output_variable_key = self.node.output_variables_key[0]
        Combo_Text_Editor(self.root, var=output_variable_key,
                          callback=self.on_output_variable_key_changed,
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=8, column=0)
        Text_Editor(self.root, var=str(self.node.timeout), callback=self.on_timeout_changed, label="timeout").grid( row=9, column=0)
        CheckBox_Editor(self.root, var=self.node.is_allow_redirects,
                        callback=self.on_allow_redirects_changed,
                        label=self.translator.get_translation("all_redirects")).grid( row=10, column=0)
        CheckBox_Editor(self.root, var=self.node.is_verify_ssl,
                        callback=self.on_verify_ssl_changed,
                        label=self.translator.get_translation("verify_ssl")).grid( row=11, column=0)


class Configer_NODE_FTP_UPLOAD(Node_Configer_Base):
    def __init__(self, node: NODE_FTP_UPLOAD, parent: TK_WINDOW, callback: Callable,
                 translator: LanguageTranslator, ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_FTP_UPLOAD, node)

    def on_host_changed(self, host: str):
        self.node.set_host(host)
        self.callback(self.node)

    def on_port_value_changed(self, port_str: str):
        self.node.set_port(int(port_str))
        self.callback(self.node)

    def on_username_changed(self, username: str):
        self.node.set_username(username)
        self.callback(self.node)

    def on_password_changed(self, password: str):
        self.node.set_password(password)
        self.callback(self.node)

    def on_remote_path_changed(self, remote_path: str):
        self.node.set_remote_path(remote_path)
        self.callback(self.node)

    def on_local_path_changed(self, local_path: str):
        self.node.set_local_path(local_path)
        self.callback(self.node)

    def on_timeout_changed(self, timeout_str: str):
        timeout = int(timeout_str)
        if timeout > 0:
            self.node.set_timeout(timeout)
            self.callback(self.node)
        else:
            messagebox.showwarning("警告", "必須為正數！")

    def on_is_tls_changed(self, is_tls: bool):
        self.node.set_is_tls(is_tls)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str] = None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        (Text_Editor(self.root, var=self.node.host, callback=self.on_host_changed, label=self.translator.get_translation("host")).
         grid(row=0,column=0, field_width=50))

        (Text_Editor(self.root, var=str(self.node.port), label=self.translator.get_translation("port"), callback=self.on_port_value_changed).
         grid(row=1, column=0, field_width=30))

        (Text_Editor(self.root, var=str(self.node.username), label=self.translator.get_translation("username"), callback=self.on_username_changed).
         grid(row=2, column=0, field_width=30))

        (Text_Editor(self.root, var=str(self.node.password), label=self.translator.get_translation("password"), callback=self.on_password_changed).
         grid(row=3, column=0, field_width=30))

        (Text_Editor(self.root, var=str(self.node.remote_path), label=self.translator.get_translation("remote_path"), callback=self.on_remote_path_changed).
         grid(row=4, column=0, field_width=50))

        (Text_Editor(self.root, var=str(self.node.local_path), label=self.translator.get_translation("local_path"),
                     callback=self.on_local_path_changed).
         grid(row=5, column=0, field_width=50))

        Text_Editor(self.root, var=str(self.node.timeout), label=self.translator.get_translation("timeout"), callback=self.on_timeout_changed).grid(
            row=6, column=0)

        CheckBox_Editor(self.root, var=self.node.is_tls, label=self.translator.get_translation("is_tls"),
                        callback=self.on_is_tls_changed).grid(row=7, column=0)

        output_variable_key=None
        if self.node.output_variables_key:
            output_variable_key = self.node.output_variables_key[0]
        Combo_Text_Editor(self.root, var=output_variable_key,
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_output_variable_key_changed).grid(row=8, column=0)

class Configer_NODE_SFTP_UPLOAD(Node_Configer_Base):
    def __init__(self, node: NODE_SFTP_UPLOAD, parent: TK_WINDOW, callback: Callable,
                 translator: LanguageTranslator, ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_SFTP_UPLOAD, node)

    def on_host_changed(self, host: str):
        self.node.set_host(host)
        self.callback(self.node)


    def on_username_changed(self, username: str):
        self.node.set_username(username)
        self.callback(self.node)

    def on_password_changed(self, password: str):
        self.node.set_password(password)
        self.callback(self.node)


    def on_remote_path_changed(self, remote_path: str, source: Enum_Text_Source):
        self.node.set_remote_path_source(source)
        match source:
            case Enum_Text_Source.COMBO:
                self.node.set_remote_path_variable_key(remote_path)
            case Enum_Text_Source.TEXT_EDITOR | Enum_Text_Source.SCROLL_TEXT_EDITOR | Enum_Text_Source.FILEPATH_SELECTOR:
                self.node.set_remote_path(remote_path)

        self.callback(self.node)

    def on_local_path_changed(self, local_path: str,source: Enum_Text_Source):
        self.node.set_local_path_source(source)
        match source:
            case Enum_Text_Source.COMBO:
                self.node.set_local_path_variable_key(local_path)
            case Enum_Text_Source.TEXT_EDITOR | Enum_Text_Source.SCROLL_TEXT_EDITOR | Enum_Text_Source.FILEPATH_SELECTOR:
                self.node.set_local_path(local_path)
        self.callback(self.node)

    def on_timeout_changed(self, timeout_str: str):
        timeout = int(timeout_str)
        if timeout > 0:
            self.node.set_timeout(timeout)
            self.callback(self.node)
        else:
            messagebox.showwarning("警告", "必須為正數！")

    def on_output_variable_key_changed(self, output_variable_key: Optional[str] = None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        row = 0
        (Text_Editor(self.root, var=self.node.host, label=self.translator.get_translation("host"), callback=self.on_host_changed).
         grid(row=row,column=0, field_width=50))

        row+=1
        (Text_Editor(self.root, var=str(self.node.username), label=self.translator.get_translation("username"), callback=self.on_username_changed).
         grid(row=row, column=0, field_width=30))

        row += 1
        (Text_Editor(self.root, var=str(self.node.password), label=self.translator.get_translation("password"), callback=self.on_password_changed).
         grid(row=row, column=0, field_width=30))

        row += 1

        source_list = [
            (Enum_Text_Source.COMBO, "V"),
            (Enum_Text_Source.TEXT_EDITOR, "C"),
            # (Enum_Text_Source.FILEPATH_SELECTOR, "F")
        ]
        Composite_Text_Sourcer(self.root, var=str(self.node.remote_path),
                               callback=self.on_remote_path_changed,
                               label=self.translator.get_translation("remote_path"),
                               enum_text_source=self.node.remote_path_source,
                               list_text_source=source_list,
                               combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=row, column=0, switch_width=40)

        row += 1

        Composite_Text_Sourcer(self.root, var=str(self.node.local_path),
                               callback=self.on_local_path_changed,
                               label=self.translator.get_translation("local_path"),
                               enum_text_source=self.node.local_path_source,
                               list_text_source=source_list,
                               combo_source=self.node.global_variables.get_list_key(),
                               is_dir=False,
                               ).grid(row=row, column=0, switch_width=40)

        row += 1
        Text_Editor(self.root, var=str(self.node.timeout), label=self.translator.get_translation("timeout"), callback=self.on_timeout_changed).grid(
            row=row, column=0)


        output_variable_key=None
        if self.node.output_variables_key:
            output_variable_key = self.node.output_variables_key[0]
        row += 1
        Combo_Text_Editor(self.root, var=output_variable_key,
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_output_variable_key_changed).grid(row=row, column=0)

class Configer_NODE_ASK_LLM(Node_Configer_Base):
    def __init__(self, node: NODE_ASK_LLM, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,
                 # llms_api: LLMS_API
                 ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_ASK_LLM, node)
        self.label_for_button_pick = translator.get_translation("pick")



    def on_llm_api_key_changed(self, llm_api_key: str):
        self.node.set_llm_api_key(llm_api_key)
        self.callback(self.node)

    def on_list_llm_api_key_changed(self, list_llm_api_key: List[str], enum_edit: Enum_Edit, i: int):
        self.node.set_list_llm_api_key(list_llm_api_key)
        self.callback(self.node)

    def on_is_multiple_llm_changed(self, is_multiple_llm: bool):
        self.node.set_is_multiple_llm(is_multiple_llm)
        self.callback(self.node)
        self.build_ui()

    def on_system_prompt_changed(self, system_prompt: str, system_prompt_source:Enum_Text_Source):
        self.node.set_system_prompt_source(system_prompt_source)
        match system_prompt_source:
            case Enum_Text_Source.COMBO:
                self.node.set_system_prompt_variable_key(system_prompt)
            case Enum_Text_Source.TEXT_EDITOR | Enum_Text_Source.SCROLL_TEXT_EDITOR:
                self.node.set_system_prompt(system_prompt)
            case Enum_Text_Source.FILEPATH_SELECTOR:
                self.node.set_system_prompt_filename( system_prompt)
        self.callback(self.node)

    def on_user_prompt_changed(self, user_prompt: str, user_prompt_source:Enum_Text_Source):
        self.node.set_user_prompt_source(user_prompt_source)
        match user_prompt_source:
            case Enum_Text_Source.COMBO:
                self.node.set_user_prompt_variable_key(user_prompt)
            case Enum_Text_Source.TEXT_EDITOR | Enum_Text_Source.SCROLL_TEXT_EDITOR:
                self.node.set_user_prompt(user_prompt)
            case Enum_Text_Source.FILEPATH_SELECTOR:
                self.node.set_user_prompt_filename(user_prompt)

        self.callback(self.node)

    def on_list_filepath_variable_key_changed(self, list_filepath_variable_key:Optional[str] = None):
        self.node.set_list_filepath_variable_key(list_filepath_variable_key)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str]= None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def on_chat_history_variable_key_changed(self, chat_history_variable_key: Optional[str] = None):
        self.node.set_chat_history_variable_key(chat_history_variable_key)
        self.callback(self.node)

    def on_chat_max_turns_variable_key_changed(self, chat_max_turns_variable_key: Optional[str] = None):
        self.node.set_chat_max_turns_variable_key(chat_max_turns_variable_key)
        self.callback(self.node)

    def on_prompt_max_length_variable_key_changed(self, prompt_max_length_variable_key: Optional[str] = None):
        self.node.set_prompt_max_length_variable_key(prompt_max_length_variable_key)
        self.callback(self.node)

    def on_temperature_changed(self, temperature):
        _temp = temperature
        if isinstance(temperature, str):
            _temp = float(temperature)
        self.node.set_temperature(_temp)
        self.callback(self.node)

    def on_is_stream_changed(self, is_stream: bool):
        self.node.set_is_stream(bool(is_stream))
        self.callback(self.node)

    def on_is_publish_changed(self, is_publish: bool):
        self.node.set_is_publish(bool(is_publish))
        self.callback(self.node)

    
    def refresh(self):
        self.build_ui()
    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        #if self.node.is_var_user_prompt and not is_string_valid(self.node.user_prompt_variable_key):
        #    self.on_user_prompt_changed(self.node.global_variables.get_list_key()[0], True)

        if self.node.llms_api and self.node.llms_api.length()>0 and (not is_string_valid(self.node.llm_api_key) or not self.node.llms_api.get_item(self.node.llm_api_key)):
            self.on_llm_api_key_changed(self.node.llms_api.get_list_key()[0])

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        index_row = 1
        CheckBox_Editor(self.root, label=self.translator.get_translation("is_multiple_llm"), var=self.node.is_multiple_llm,
                        callback=self.on_is_multiple_llm_changed).grid(row=index_row, column=0)
        index_row += 1

        if self.node.llms_api and self.node.llms_api.length()>0:
            if self.node.is_multiple_llm:
                ttk.Label(self.root, text=self.translator.get_translation("LLM")).grid(row=index_row, column=0,sticky="w")
                index_row += 1

                List_Editor_Combo(self.root, var=self.node.list_llm_api_key,
                                  callback=self.on_list_llm_api_key_changed,
                                  combo_source=self.node.llms_api.get_list_key(),
                                  ).grid(row=index_row, column=0)
                index_row += 1

                ttk.Label(self.root, text=self.translator.get_translation("summary_llm")).grid(row=index_row, column=0,
                                                                                       sticky="w")
                index_row += 1

            Combo_Text_Editor(self.root, var=self.node.llm_api_key, label="LLM", callback=self.on_llm_api_key_changed,
                                combo_source= self.node.llms_api.get_list_key(),
                                ).grid(row=index_row, column=0)

        else:
            ttk.Label(self.root, text=self.translator.get_translation("no_llms_api_available")).grid(row=index_row, column=0,
                                                                                                  sticky="w")
        index_row += 1
        self.checkbox_is_stream = CheckBox_Editor(self.root, label=self.translator.get_translation("is_stream"), var=self.node.is_stream,
                                                  callback=self.on_is_stream_changed).grid(
            row=index_row, column=0)
        index_row += 1
        CheckBox_Editor(self.root, var=self.node.is_publish,
                        label=self.translator.get_translation("is_publish"),
                        callback=self.on_is_publish_changed).grid(row=index_row, column=0)

        source_list = [
            (Enum_Text_Source.COMBO, "V"),
            (Enum_Text_Source.SCROLL_TEXT_EDITOR, "C"),
           # (Enum_Text_Source.FILEPATH_SELECTOR, "F")
        ]

        index_row += 1
        ttk.Label(self.root, text=self.translator.get_translation("system_prompt")).grid(row=index_row, column=0, sticky="w")
        index_row += 1
        system_prompt = self.node.system_prompt
        match self.node.system_prompt_source:
            case Enum_Text_Source.COMBO:
                system_prompt=self.node.system_prompt_variable_key
            case Enum_Text_Source.FILEPATH_SELECTOR:
                system_prompt = self.node.system_prompt_filename

        Composite_Text_Sourcer(self.root, var=system_prompt,
                              callback=self.on_system_prompt_changed,
                               enum_text_source=self.node.system_prompt_source,
                                list_text_source = source_list,
                             combo_source=self.node.global_variables.get_list_key(),
                               label_for_button_pick=self.translator.get_translation("pick")
                            ).grid( row=index_row, column=0, switch_width=40)

        index_row += 1
        ttk.Label(self.root, text=self.translator.get_translation("user_prompt")).grid(row=index_row, column=0,
                                                                                         sticky="w")
        index_row += 1
        user_prompt = self.node.user_prompt
        match self.node.user_prompt_source:
            case Enum_Text_Source.COMBO:
                user_prompt = self.node.user_prompt_variable_key
            case Enum_Text_Source.FILEPATH_SELECTOR:
                user_prompt = self.node.user_prompt_filename

        Composite_Text_Sourcer(self.root, var=user_prompt,
                               callback=self.on_user_prompt_changed,
                               enum_text_source=self.node.user_prompt_source,
                               list_text_source=source_list,
                               combo_source=self.node.global_variables.get_list_key(),
                               label_for_button_pick=self.translator.get_translation("pick")
                               ).grid(row=index_row, column=0, switch_width=40)

        index_row += 1
        Combo_Text_Editor(self.root, var=self.node.list_filepath_variable_key,
                                label=self.translator.get_translation("list_filepath_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(ENUM_VARIABLE.LIST),
                                callback=self.on_list_filepath_variable_key_changed,
                          is_nullable=True, null_str=self.translator.get_translation("none")).grid(row=index_row, column=0)
        index_row += 1
        Combo_Text_Editor(self.root, var=self.node.chat_history_variable_key,
                          label=self.translator.get_translation("chat_history_variable_key"),
                          combo_source=self.node.global_variables.get_list_key(),
                          callback=self.on_chat_history_variable_key_changed,
                          is_nullable=True, null_str=self.translator.get_translation("none")).grid(row=index_row, column=0)
        index_row += 1
        Combo_Text_Editor(self.root, var=self.node.chat_max_turns_variable_key,
                          label=self.translator.get_translation("chat_max_turns_variable_key"),
                          combo_source=self.node.global_variables.get_list_key(),
                          callback=self.on_chat_max_turns_variable_key_changed,
                          is_nullable=True, null_str=self.translator.get_translation("none")).grid(row=index_row, column=0)
        index_row += 1
        Combo_Text_Editor(self.root, var=self.node.prompt_max_length_variable_key,
                          label=self.translator.get_translation("prompt_max_length_variable_key"),
                          combo_source=self.node.global_variables.get_list_key(),
                          callback=self.on_prompt_max_length_variable_key_changed,
                          is_nullable=True, null_str=self.translator.get_translation("none")).grid(row=index_row, column=0)
        index_row += 1
        Combo_Text_Editor(self.root, var=self.node.output_variables_key[0],
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                          is_nullable=True,
                          null_str=self.translator.get_translation("none"),
                                callback=self.on_output_variable_key_changed).grid(row=index_row, column=0)
        index_row += 1
        Slider(self.root, label="Temperature", callback=self.on_temperature_changed,
               legend1=self.translator.get_translation("accuracy"),
               legend2=self.translator.get_translation("creativity"), min_var=0.5, max_var=1.5, step=0.1,
               var=self.node.temperature).grid(row=index_row, column=0)

        #Text_Editor(self.root, text=str(self.node.temperature), label="Temperature", callback=self.on_temperature_changed).grid( row=10, column=0)


class Configer_NODE_CATEGORIZE_BY_LLM(Node_Configer_Base):
    def __init__(self, node: NODE_CATEGORIZED_BY_LLM, parent:TK_WINDOW, callback:Callable,
                 translator: LanguageTranslator,
                 #llms_api: LLMS_API,
                 # global_variables:VARIABLES
                 ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_CATEGORIZED_BY_LLM, node)
        #self.llms_api = llms_api

    #def on_system_prompt_mid_changed(self, system_prompt_mid: str):
    #    self.node.set_system_prompt_mid(system_prompt_mid)
    #    self.callback(self.node)

    def on_system_prompt_head_changed(self, system_prompt: str):
        self.node.set_system_prompt_head(system_prompt)
        self.callback(self.node)

    def on_system_prompt_tail_changed(self, system_prompt: str):
        self.node.set_system_prompt_tail(system_prompt)
        self.callback(self.node)

    def on_list_category_changed(self, list_category, source: Enum_Text_Source):
        self.node.set_list_category_source(source)
        match source:
            case Enum_Text_Source.COMBO:
                self.node.set_list_category_variable_key(list_category)
            case Enum_Text_Source.LIST_EDITOR_TEXT :
                self.node.set_list_category(list_category)

        self.callback(self.node)

    def on_index_variable_key_changed(self, index_variable_key: str):
        self.node.set_index_variable_key(index_variable_key)
        self.callback(self.node)

    def on_llm_reply_variable_key_changed(self, llm_reply_variable_key: str):
        self.node.set_llm_reply_variable_key(llm_reply_variable_key)
        self.callback(self.node)
    #def on_list_category_changed(self, list_category: List[str], enum_edit: Enum_Edit, i: int):
    #    self.node.set_list_category(list_category)
    #    self.node.set_next_nodes_number(len(list_category))
    #    self.callback(self.node)
    #def on_variable_name_to_be_categorized_changed(self, variable_name):
    #    self.node.set_variable_name_to_be_categorized(variable_name)
    #    self.callback(self.node)

    def on_llm_api_key_changed(self, llm_api_key):
        self.node.set_llm_api_key(llm_api_key)
        self.callback(self.node)

    def on_is_branch_changed(self, is_branch):
        self.node.set_is_branch(is_branch)
        self.callback(self.node)

    def on_node_changed(self, node: WORK_NODE):
        self.node = node
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)
    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        #if not is_string_valid(self.node.variable_name_to_be_categorized):
        #   self.on_variable_name_to_be_categorized_changed( self.node.global_variables.get_list_key()[0])

        if self.node.llms_api and self.node.llms_api.length() > 0 and (
                not is_string_valid(self.node.llm_api_key) or not self.node.llms_api.get_item(self.node.llm_api_key)):
            self.on_llm_api_key_changed(self.node.llms_api.get_list_key()[0])


        if self.node.llms_api:
            Combo_Text_Editor(self.root, var=self.node.llm_api_key, label="LLM",
                                    callback=self.on_llm_api_key_changed,
                                    combo_source=self.node.llms_api.get_list_key(),
                                    ).grid(row=0, column=0)
        else:
            ttk.Label(self.root, text=self.translator.get_translation("no_llms_api_available")).grid(row=0, column=0,
                                                                                                     sticky="w")

        #if not is_string_valid(self.node.list_category_variable_key) :
        #    self.on_list_category_variable_key_changed(self.node.global_variables.get_list_array_name()[0])

        ttk.Label(self.root, text=self.translator.get_translation("system_prompt_head")).grid(row=1, column=0, sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.system_prompt_head, callback=self.on_system_prompt_head_changed).grid(
            row=2, column=0)

        source_list = [
            (Enum_Text_Source.COMBO, "V"),
            (Enum_Text_Source.LIST_EDITOR_TEXT, "C"),
        ]
        var = self.node.list_category if self.node.list_category_source == Enum_Text_Source.LIST_EDITOR_TEXT else self.node.list_category_variable_key
        Composite_Text_Sourcer(self.root, var=var,
                               callback=self.on_list_category_changed,
                               label=self.translator.get_translation("list_category"),
                               enum_text_source=self.node.list_category_source,
                               list_text_source=source_list,
                               combo_source=self.node.global_variables.get_list_key(),
                               ).grid(row=3, column=0, switch_width=50, switch_height=25, field_width=40)

        ttk.Label(self.root, text=self.translator.get_translation("system_prompt_tail")).grid(row=4, column=0, sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.system_prompt_tail, callback=self.on_system_prompt_tail_changed).grid(
            row=5, column=0)

        Combo_Text_Editor(self.root, label=self.translator.get_translation("store_index_in_variable"),
                          var=self.node.index_variable_key,
                          is_nullable=True,
                          null_str=self.translator.get_translation("none"),
                          combo_source=self.node.global_variables.get_list_key(),
                          callback=self.on_index_variable_key_changed).grid(row=6, column=0)

        Combo_Text_Editor(self.root, label=self.translator.get_translation("store_llm_reply_in_variable"),
                          var=self.node.llm_reply_variable_key,
                          is_nullable=True,
                          null_str=self.translator.get_translation("none"),
                          combo_source=self.node.global_variables.get_list_key(),
                          callback=self.on_llm_reply_variable_key_changed).grid(row=7, column=0)

        CheckBox_Editor(self.root,
                        label=self.translator.get_translation("is_branch"),
                        var=self.node.is_branch,
                        callback=self.on_is_branch_changed).grid(row=8, column=0, sticky="w")


class Configer_NODE_KNOWLEDGE_RETRIEVER(Node_Configer_Base):
    def __init__(self, node: NODE_KNOWLEDGE_RETRIEVER, parent:TK_WINDOW, callback:Callable, #list_embed_model_name: List[str],
                 # list_collection_name: List[str],
                 translator: LanguageTranslator,
                 knowledge_collections: Optional[KNOWLEDGE_COLLECTIONS]=None,
               #  llms_api: Optional[LLMS_API] = None,
               #  global_variables: Optional[VARIABLES] = None,
                 ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_KNOWLEDGE_RETRIEVER, node)
        #self.node.set_llms_api(llms_api=llms_api)

        self.knowledge_collections = knowledge_collections
        self.list_collection_name = self.knowledge_collections.get_list_collection_name()

        list_collection_name = self.node.list_collection_name


        if list_collection_name and len(list_collection_name)>0:
            list_new_collection_name=[]
            for collection_name in list_collection_name:
               if self.knowledge_collections.is_key_existed(collection_name):
                   list_new_collection_name.append(collection_name)
            self.node.set_list_collection_name(list_new_collection_name)

       # self.llms_api = llms_api

    #def on_is_stream_changed(self, is_stream: bool):
    #    self.node.set_is_stream(bool(is_stream))
    #    self.callback(self.node)

    def on_input_variable_key_changed(self, input_variable_key:str):
        self.node.set_input_variable_key(input_variable_key)
        self.callback(self.node)

    def on_list_collection_name_changed(self, list_collection_name: List[str], enum_edit:Enum_Edit, index:int):
        self.node.set_list_collection_name(list_collection_name)
        self.callback(self.node)

    def on_llm_api_key_changed(self, llm_api_key):
        self.node.set_llm_api_key(llm_api_key)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str] = None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)
        #ttk.Label(self.root, text=self.translator.get_translation("embed_model")).grid(row=1, column=0)
        if not is_string_valid(self.node.input_variable_key):
            self.on_input_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        #if len(self.node.list_collection_name)==0 or not is_string_valid(self.node.list_collection_name[0]):
        #    self.on_list_collection_name_changed([self.knowledge_collections.get_list_collection_name()[0]])

        if self.node.llms_api and self.node.llms_api.length() > 0 and (
                not is_string_valid(self.node.llm_api_key) or not self.node.llms_api.get_item(self.node.llm_api_key)):
            self.on_llm_api_key_changed(self.node.llms_api.get_list_key()[0])

        if self.node.llms_api:
            Combo_Text_Editor(self.root, label="LLM",
                                    var=self.node.llm_api_key,
                                    combo_source=self.node.llms_api.get_list_key(),
                                    callback=self.on_llm_api_key_changed,
                                    ).grid(row=0, column=0)
        else:
            ttk.Label(self.root, text=self.translator.get_translation("no_llms_api_available")).grid(row=0, column=0,
                                                                                                     sticky="w")
        Combo_Text_Editor(self.root, var=self.node.input_variable_key,
                                label=self.translator.get_translation("input_variable"),
                                callback=self.on_input_variable_key_changed,
                          combo_source=self.node.global_variables.get_list_key()).grid( row=1, column=0)
        #ttk.Label(self.root, text=self.translator.get_translation("persist_directory")).grid(row=2, column=0)
        #Text_Editor(self.root, text=self.node.persist_directory, callback=self.on_persist_directory_changed).grid( row=2,
        #            column=1)
        ttk.Label(self.root, text=self.translator.get_translation("knowledge_collections")).grid(row=2, column=0, sticky="w")
        self.list_collection_name = None
        if self.node.list_collection_name and len(self.node.list_collection_name)>0:
            self.list_collection_name = self.knowledge_collections.get_list_collection_name_same_group(self.node.list_collection_name[0])
        else:
            self.list_collection_name = self.knowledge_collections.get_list_collection_name()

        if self.list_collection_name and len(self.list_collection_name)>0:
            List_Editor_Combo(self.root, var=self.node.list_collection_name,
                                   combo_source=self.list_collection_name,
                                   callback=self.on_list_collection_name_changed).grid(row=3, column=0)
        else:
            ttk.Label(self.root, text=self.translator.get_translation("add_knowledge_collections")).grid(row=3, column=0,
                                                                                                     sticky="w")

        Combo_Text_Editor(self.root, var=self.node.output_variables_key[0],
                                label=self.translator.get_translation("output_variable"),
                          combo_source= self.node.global_variables.get_list_key(),
                          callback=self.on_output_variable_key_changed).grid(row=4, column=0)

        #CheckBox_Editor(self.root, label="Stream", value=self.node.is_stream,
        #                callback=self.on_is_stream_changed).grid(row=5, column=0)

#class Configer_NODE_ASK_LLM_WITH_KNOWLEDGE(Node_Configer_Base):
#    def __init__(self, node: NODE_ASK_LLM_WITH_KNOWLEDGE, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,
#                 #llms_api: LLMS_API,
#                 #global_variables:VARIABLES
#                 ):
#        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
#
#        self.node = cast(NODE_ASK_LLM_WITH_KNOWLEDGE, node)
#
#        #self.llms_api = llms_api
#        #self.node.set_llms_api(llms_api)
#
#    def on_system_prompt_mid_changed(self, system_prompt_mid: str):
#        self.node.set_system_prompt_mid(system_prompt_mid)
#        self.callback(self.node)
#
#    def on_knowledge_variable_key_changed(self, knowledge_variable_key: str):
#        self.node.set_knowledge_variable_key(knowledge_variable_key)
#        self.callback(self.node)
#
#    def on_node_changed(self, node: WORK_NODE):
#        self.node = node
#        self.callback(self.node)
#
#    def refresh(self):
#        self.build_ui()
#
#    def destroy(self):
#        destroy_TK_WINDOW(self.root)
#
#    def build_ui(self):
#        destroy_TK_WINDOW(self.root, is_destroy_root=False)
#        Configer_NODE_ASK_LLM(self.node, self.root, callback=self.on_node_changed,
#                              #llms_api=self.node.llms_api,
#                              # global_variables=self.node.global_variables,
#                              translator=self.translator).grid(row=0, column=0)
#        ttk.Label(self.root, text=self.translator.get_translation("system_prompt_mid")).grid(row=1, column=0, sticky="w")
#        Scroll_Text_Editor(self.root, text=self.node.system_prompt_mid, callback=self.on_system_prompt_mid_changed).grid(
#                           row=2, column=0)
#
#        Combo_Text_Editor(self.root, text=self.node.knowledge_variable_key,
#                                label=self.translator.get_translation("knowledge_variables_key"),
#                          combo_source= self.node.global_variables.get_list_key(),
#                          callback=self.on_knowledge_variable_key_changed).grid(row=3, column=0)
#
#
class Configer_NODE_OCR(Node_Configer_Base):
    def __init__(self, node: NODE_OCR, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator
                ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_OCR, node)

    def on_list_language_key_changed(self, list_language_key: List[str], enum_edit:Enum_Edit, i:int):
        self.node.set_list_language_key(list_language_key)
        self.callback(self.node)

    def on_image_filepath_variable_key_changed(self, filepath_variable_key: Optional[str] = None):
        self.node.set_image_filepath_variable_key(filepath_variable_key)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str]= None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        if not is_string_valid(self.node.image_filepath_variable_key):
            self.on_image_filepath_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        ttk.Label(self.root, text=self.translator.get_translation("list_language")).grid(row=1, column=0, sticky="w")
        List_Editor_Combo(self.root, callback=self.on_list_language_key_changed,
                               var=self.node.list_language_key,
                               combo_source=[key for key in dict_EasyOCR_languages.keys()],
                               ).grid(row=2, column=0)

        Combo_Text_Editor(self.root, var=self.node.image_filepath_variable_key,
                                label=self.translator.get_translation("image_filepath_variables_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_image_filepath_variable_key_changed).grid(row=3, column=0)

        Combo_Text_Editor(self.root, var=self.node.output_variables_key[0],
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_output_variable_key_changed).grid(row=4, column=0)

class Configer_NODE_VOICE_RECOGNIZE(Node_Configer_Base):
    def __init__(self, node: NODE_VOICE_RECOGNIZE, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator
                ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_VOICE_RECOGNIZE, node)

    def on_language_key_changed(self, language_variable_key: str):
        self.node.set_language_key(language_variable_key)
        self.callback(self.node)

    def on_voice_filepath_variable_key_changed(self, voice_filepath_variable_key: Optional[str] = None):
        self.node.set_voice_filepath_variable_key(voice_filepath_variable_key)
        self.callback(self.node)

    def on_output_variable_key_changed(self, output_variable_key: Optional[str]= None):
        self.node.set_output_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        if not is_string_valid(self.node.voice_filepath_variable_key):
            self.on_voice_filepath_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if len(self.node.output_variables_key) == 0 or not is_string_valid(self.node.output_variables_key[0]):
            self.on_output_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root, callback=self.on_language_key_changed, var=self.node.language_key,
                                combo_source=[key for key in dict_VoiceRecognition_languages.keys()],
                                label=self.translator.get_translation("language"),
                                ).grid(row=1, column=0)

        Combo_Text_Editor(self.root, var=self.node.voice_filepath_variable_key,
                                label=self.translator.get_translation("voice_filepath_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_voice_filepath_variable_key_changed).grid(row=2, column=0)

        Combo_Text_Editor(self.root, var=self.node.output_variables_key[0],
                                label=self.translator.get_translation("output_variable"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_output_variable_key_changed).grid(row=3, column=0)

class Configer_NODE_GENERATE_IMAGE_FROM_TEXT(Node_Configer_Base):
    def __init__(self, node: NODE_GENERATE_IMAGE_FROM_TEXT, parent: TK_WINDOW, callback:Callable, translator: LanguageTranslator
                ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)
        self.node = cast(NODE_GENERATE_IMAGE_FROM_TEXT, node)

    def on_image_prompt_variable_key_changed(self, image_prompt_variable_key: Optional[str] = None):
        self.node.set_image_prompt_variable_key(image_prompt_variable_key)
        self.callback(self.node)

    def on_image_width_variable_key_changed(self, image_width_variable_key: Optional[str] = None):
        self.node.set_image_width_variable_key(image_width_variable_key)
        self.callback(self.node)

    def on_image_height_variable_key_changed(self, image_height_variable_key: Optional[str] = None):
        self.node.set_image_height_variable_key(image_height_variable_key)
        self.callback(self.node)

    def on_inference_steps_variable_key_changed(self, inference_steps_variable_key: Optional[str] = None):
        self.node.set_inference_steps_variable_key(inference_steps_variable_key)
        self.callback(self.node)

    def on_guidance_scale_variable_key_changed(self, guidance_scale_variable_key: Optional[str] = None):
        self.node.set_guidance_scale_variable_key(guidance_scale_variable_key)
        self.callback(self.node)

    def on_seed_variable_key_changed(self, seed_variable_key: Optional[str] = None):
        self.node.set_seed_variable_key(seed_variable_key)
        self.callback(self.node)

    def on_output_filepath_variable_key_changed(self, output_variable_key: Optional[str]= None):
        self.node.set_output_filepath_variable_key(output_variable_key)
        self.callback(self.node)

    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        if not is_string_valid(self.node.image_prompt_variable_key):
            self.on_image_prompt_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if not is_string_valid(self.node.image_width_variable_key):
                self.on_image_width_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if not is_string_valid(self.node.image_height_variable_key):
                self.on_image_height_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if not is_string_valid(self.node.image_height_variable_key):
                self.on_image_height_variable_key_changed(self.node.global_variables.get_list_key()[0])

        if not is_string_valid(self.node.output_filepath_variable_key):
            self.on_output_filepath_variable_key_changed(self.node.global_variables.get_list_key()[0])

        Combo_Text_Editor(self.root, var=self.node.image_prompt_variable_key,
                                label=self.translator.get_translation("image_prompt_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_image_prompt_variable_key_changed).grid(row=0, column=0)

        Combo_Text_Editor(self.root, var=self.node.image_width_variable_key,
                                label=self.translator.get_translation("image_width_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_image_width_variable_key_changed).grid(row=1, column=0)

        Combo_Text_Editor(self.root, var=self.node.image_height_variable_key,
                                label=self.translator.get_translation("image_height_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_image_height_variable_key_changed).grid(row=2, column=0)

        Combo_Text_Editor(self.root, var=self.node.inference_steps_variable_key,
                                label=self.translator.get_translation("inference_steps_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_inference_steps_variable_key_changed).grid(row=3, column=0)

        Combo_Text_Editor(self.root, var=self.node.guidance_scale_variable_key,
                                label=self.translator.get_translation("guidance_scale_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_guidance_scale_variable_key_changed).grid(row=4, column=0)

        #Combo_Text_Editor(self.root, text=self.node.seed_variable_key,
        #                        label=self.translator.get_translation("seed_variable_key"),
        #                        combo_source=self.node.global_variables.get_list_key(),
        #                        callback=self.on_seed_variable_key_changed).grid(row=5, column=0)

        Combo_Text_Editor(self.root, var=self.node.output_filepath_variable_key,
                                label=self.translator.get_translation("output_filepath_variable_key"),
                                combo_source=self.node.global_variables.get_list_key(),
                                callback=self.on_output_filepath_variable_key_changed()).grid(row=6, column=0)


class Configer_NODE_TRANSLATED_BY_LLM(Node_Configer_Base):
    def __init__(self, node: NODE_TRANSLATED_BY_LLM, parent:TK_WINDOW, callback:Callable, translator: LanguageTranslator,
                # llms_api: LLMS_API,
                 #global_variables:VARIABLES
                 ):
        super().__init__(node=node, parent=parent, callback=callback, translator=translator)

        self.node = cast(NODE_TRANSLATED_BY_LLM, node)
        #self.llms_api = llms_api
       # self.node.set_llms_api(llms_api)

        self.list_language = None
        self.is_target_same_folder_as_source = True
        self.source_filepath = ""

        self.target_folder = ""
        self.target_filename = ""

        if is_string_valid(self.node.target_filepath):
            dirname, filename ,_ext = get_dir_filename_ext(self.node.target_filepath)
            ext = self.check_ext(_ext)
            self.target_filename =filename+ ext
            if ext != _ext:
                self.on_target_filename_changed(filename+ ext)

            self.target_folder = dirname
            self.is_target_same_folder_as_source = False

        if is_string_valid(self.node.source_filepath):
            dirname, filename, ext = get_dir_filename_ext(self.node.source_filepath)
            if self.is_target_same_folder_as_source:
                self.target_folder = dirname
            elif self.target_folder == dirname:
                self.is_target_same_folder_as_source = True
        self._get_list_language_from_glossary(self.node.glossary_filepath)
        self.target_filename_editor=None

    def _get_list_language_from_glossary(self, glossary_filepath):
        if glossary_filepath:
            try:
                df = pd.read_excel(glossary_filepath)
                self.list_language = list(df.columns)

            except Exception as e:
                print(f"詞典建立失敗:{glossary_filepath}{str(e)}")
        else:
            self.list_language = []


    def on_glossary_filepath_changed(self, filepath: str):
        self.node.set_glossary_filepath(filepath)
        self._get_list_language_from_glossary(self.node.glossary_filepath)
        self.callback(self.node)
        self.build_ui()

    def on_source_filepath_changed(self, filepath: str):
        self.source_filepath=filepath
        self.node.set_source_filepath(filepath)
        self.callback(self.node)
        self.check_and_save_target_filepath()

    def on_target_folder_changed(self, folder: str):
        self.target_folder = folder
        self.check_and_save_target_filepath()

    def on_target_filename_changed(self, name: str):
        self.target_filename = name
        self.check_and_save_target_filepath()

    def check_ext(self, ext):
        match ext:
            case ".doc" | ".xls" | ".ppt":
                ext += "x"
        return ext

    def check_and_save_target_filepath(self):
        if is_string_valid(self.node.source_filepath) and self.is_target_same_folder_as_source:
            dirname, filename, ext = get_dir_filename_ext(self.node.source_filepath)
            self.target_folder = dirname

        if is_string_valid(self.target_filename) and is_string_valid(
                self.source_filepath):
            _, source_ext = get_filename_ext(self.source_filepath)

            source_ext = self.check_ext(source_ext)

            target_primary, _ = get_filename_ext(self.target_filename)
            self.target_filename = target_primary + source_ext
            self.target_filename_editor.configure(text=self.target_filename)

        if is_string_valid(self.target_folder) and is_string_valid(self.target_filename):
            self.node.set_target_filepath(self.target_folder + '/'+ self.target_filename)
            self.callback(self.node)

    def on_source_lang_changed(self, lang: str):
        self.node.set_source_lang(lang)
        self.callback(self.node)

    def on_target_lang_changed(self, lang: str):
        self.node.set_target_lang(lang)
        self.callback(self.node)

    def on_llm_api_key_changed(self, llm_api_key):
        self.node.set_llm_api_key(llm_api_key)
        self.callback(self.node)

    def on_temperature_changed(self, temperature):
        _temp = temperature
        if isinstance(temperature, str):
            _temp = float(temperature)
        self.node.set_temperature(_temp)
        self.callback(self.node)

    def on_delta_font_size_changed(self, delta_font_size):
        _delta = delta_font_size
        if isinstance(delta_font_size, str):
            try:
                _delta = float(delta_font_size)
            except Exception as e:
                _delta = 0
        self.node.set_delta_font_size(_delta)
        self.callback(self.node)

    def on_is_target_same_folder_as_source_changed(self, is_same:bool):
        self.is_target_same_folder_as_source = is_same
        self.build_ui()

    def on_note_changed(self, note: str):
        self.node.set_note(note)
        self.callback(self.node)

    def on_style_changed(self, style: str):
        self.node.set_style(style)
        self.callback(self.node)

    def on_node_changed(self, node: WORK_NODE):
        self.node = node
        self.callback(self.node)


    def refresh(self):
        self.build_ui()

    def destroy(self):
        destroy_TK_WINDOW(self.root)

    def build_ui(self):
        destroy_TK_WINDOW(self.root, is_destroy_root=False)

        if not is_string_valid(self.node.source_lang) and self.list_language and len(self.list_language)>0:
            self.on_source_lang_changed(self.list_language[0])

        if not is_string_valid(self.node.target_lang) and self.list_language and len(self.list_language)>0:
            self.on_target_lang_changed(self.list_language[0])

        Filepath_Selector(self.root,
                          label=self.translator.get_translation("glossary_filepath"),
                                                   file_path=self.node.glossary_filepath, is_dir=False,
                                                   callback=self.on_glossary_filepath_changed,
                                                   label_for_button_pick=self.translator.get_translation("pick")).grid(
            row=1, column=0)

        Filepath_Selector(self.root,
                          label=self.translator.get_translation("source_filepath"),
                          file_path=self.node.source_filepath, is_dir=False,
                          callback=self.on_source_filepath_changed,
                          label_for_button_pick=self.translator.get_translation("pick")).grid(
            row=2, column=0)


        CheckBox_Editor(self.root,
                        label=self.translator.get_translation("target_same_folder_as_source"),
                        var=self.is_target_same_folder_as_source,
                        callback=self.on_is_target_same_folder_as_source_changed).grid(row=3, column=0,
                                                                                           sticky="w")

        if not self.is_target_same_folder_as_source:
            ttk.Label(self.root, text=self.translator.get_translation("target_folder")).grid(row=4, column=0,
                                                                                                sticky="w")
            Filepath_Selector(self.root,
                              file_path=self.target_folder, is_dir=True,
                              callback=self.on_target_folder_changed,
                              label_for_button_pick=self.translator.get_translation("pick")).grid(
                row=5, column=0)

        self.target_filename_editor = Text_Editor(self.root, var=self.target_filename, label=self.translator.get_translation("target_filename"),
                          callback=self.on_target_filename_changed).grid(row=6, column=0, field_width=20)

        if self.list_language and len(self.list_language)>0:
            Combo_Text_Editor(self.root, var=self.node.source_lang,
                                    label=self.translator.get_translation("source_lang"),
                              combo_source= self.list_language,
                              callback=self.on_source_lang_changed).grid(row=7, column=0)

            Combo_Text_Editor(self.root, var=self.node.target_lang,
                                    label=self.translator.get_translation("target_lang"),
                                    combo_source=self.list_language,
                                    callback=self.on_target_lang_changed).grid(row=8, column=0)
        else:
            ttk.Label(self.root, text=self.translator.get_translation("set_glossary_filepath")).grid(row=7, column=0,
                                                                                                 sticky="w")


        ttk.Label(self.root, text=self.translator.get_translation("translation_note")).grid(row=9, column=0,
                                                                                                 sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.note,
                           callback=self.on_note_changed).grid(row=10, column=0)

        ttk.Label(self.root, text=self.translator.get_translation("translation_writing_style")).grid(row=11, column=0,
                                                                                            sticky="w")
        Scroll_Text_Editor(self.root, var=self.node.style,
                           callback=self.on_style_changed).grid(row=12, column=0)

        if self.node.llms_api and self.node.llms_api.length() > 0 and (
                not is_string_valid(self.node.llm_api_key) or not self.node.llms_api.get_item(self.node.llm_api_key)):
            self.on_llm_api_key_changed(self.node.llms_api.get_list_key()[0])

        if self.node.llms_api:
            Combo_Text_Editor(self.root, var=self.node.llm_api_key, label="LLM", callback=self.on_llm_api_key_changed,
                              combo_source=self.node.llms_api.get_list_key(),
                              ).grid(row=13, column=0)
        else:
            ttk.Label(self.root, text=self.translator.get_translation("no_llms_api_available")).grid(row=13, column=0,
                                                                                                     sticky="w")
        Slider(self.root, label="Temperature", callback=self.on_temperature_changed, legend1=self.translator.get_translation("accuracy"),
               legend2=self.translator.get_translation("creativity"), min_var=0.5, max_var=1.5, step=0.1, var=self.node.temperature).grid( row=14, column=0)
        #Text_Editor(self.root, text=str(self.node.temperature), label="Temperature", callback=self.on_temperature_changed).grid( row=14, column=0)
        Text_Editor(self.root, var=str(self.node.delta_font_size),
                    label=self.translator.get_translation("delta_font_size"),
                    callback=self.on_delta_font_size_changed).grid( row=15, column=0)