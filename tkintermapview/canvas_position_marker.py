import tkinter
import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .map_widget import TkinterMapView

from .utility_functions import decimal_to_osm, osm_to_decimal


class CanvasPositionMarker:
    def __init__(self,
                 map_widget: "TkinterMapView",
                 position: tuple,
                 text: str = None,
                 text_color: str = "#652A22",
                 font=None,
                 marker_color_circle: str = "#9B261E",
                 marker_color_outside: str = "#C5542D",
                 command: Callable = None,
                 image: tkinter.PhotoImage = None,
                 icon: tkinter.PhotoImage = None,
                 icon_anchor: str = "center",
                 image_zoom_visibility: tuple = (0, float("inf")),
                 data: any = None):

        self.map_widget = map_widget
        self.position = position
        self.text_color = text_color
        self.marker_color_circle = marker_color_circle
        self.marker_color_outside = marker_color_outside
        self.text = text
        self.text_y_offset = 0  # vertical offset pf text from marker position in px
        self.image = image
        self.icon = icon
        self.icon_anchor = icon_anchor  # can be center, n, nw, w, sw, s, ew, e, ne
        self.image_hidden = False
        self.image_zoom_visibility = image_zoom_visibility
        self.deleted = False
        self.command = command
        self.data = data

        self.polygon = None
        self.big_circle = None
        self.canvas_text = None
        self.canvas_image = None
        self.canvas_icon = None

        if font is None:
            if sys.platform == "darwin":
                self.font = "Tahoma 13 bold"
            else:
                self.font = "Tahoma 11 bold"
        else:
            self.font = font

        self.calculate_text_y_offset()

    def calculate_text_y_offset(self):
        if self.icon is not None:
            if self.icon_anchor in ("center", "e", "w"):
                self.text_y_offset = -round(self.icon.height() / 2) - 5
            elif self.icon_anchor in ("nw", "n", "ne"):
                self.text_y_offset = -5
            elif self.icon_anchor in ("sw", "s", "se"):
                self.text_y_offset = -self.icon.height() - 5
            else:
                raise ValueError(f"CanvasPositionMarker: wring anchor value: {self.icon_anchor}")
        else:
            self.text_y_offset = -56

    def delete(self):
        if self in self.map_widget.canvas_marker_list:
            self.map_widget.canvas_marker_list.remove(self)

        self.map_widget.canvas.delete(self.polygon)
        self.map_widget.canvas.delete(self.big_circle)
        self.map_widget.canvas.delete(self.canvas_text)
        self.map_widget.canvas.delete(self.canvas_icon)
        self.map_widget.canvas.delete(self.canvas_image)

        self.polygon, self.big_circle, self.canvas_text, self.canvas_image, self.canvas_icon = None, None, None, None, None
        self.deleted = True
        self.map_widget.canvas.update()

    def set_position(self, deg_x, deg_y):
        self.position = (deg_x, deg_y)
        self.draw()

    def set_text(self, text):
        self.text = text
        self.draw()

    def change_icon(self, new_icon: tkinter.PhotoImage):
        if self.icon is None:
            raise AttributeError("CanvasPositionMarker: marker needs icon image in constructor to change icon image later")
        else:
            self.icon = new_icon
            self.calculate_text_y_offset()
            self.map_widget.canvas.itemconfigure(self.canvas_icon, image=self.icon)

    def hide_image(self, image_hidden: bool):
        self.image_hidden = image_hidden
        self.draw()

    def mouse_enter(self, event=None):
        if sys.platform == "darwin":
            self.map_widget.canvas.config(cursor="pointinghand")
        elif sys.platform.startswith("win"):
            self.map_widget.canvas.config(cursor="hand2")
        else:
            self.map_widget.canvas.config(cursor="hand2")  # not tested what it looks like on Linux!

    def mouse_leave(self, event=None):
        self.map_widget.canvas.config(cursor="arrow")

    def click(self, event=None):
        if self.command is not None:
            self.command(self)

    def get_canvas_pos(self, position):    # 這個可以將經緯度轉成 canvas 的上的座標。
        tile_position = decimal_to_osm(*position, round(self.map_widget.zoom))

        widget_tile_width = self.map_widget.lower_right_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]
        widget_tile_height = self.map_widget.lower_right_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]

        canvas_pos_x = ((tile_position[0] - self.map_widget.upper_left_tile_pos[0]) / widget_tile_width) * self.map_widget.width
        canvas_pos_y = ((tile_position[1] - self.map_widget.upper_left_tile_pos[1]) / widget_tile_height) * self.map_widget.height

        return canvas_pos_x, canvas_pos_y

    def draw(self, event=None):
        # 獲取標記在畫布上的位置
        canvas_pos_x, canvas_pos_y = self.get_canvas_pos(self.position)
        # 檢查標記是否被刪除以及是否在畫布的可視範圍內
        if not self.deleted:
            if 0 - 50 < canvas_pos_x < self.map_widget.width + 50 and 0 < canvas_pos_y < self.map_widget.height + 70:

                # draw icon image for marker
                # 如果有指定圖標，則繪製圖像
                if self.icon is not None:
                    if self.canvas_icon is None:
                        # 在畫布上創建圖像並設置相關屬性
                        self.canvas_icon = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y,
                                                                               anchor=self.icon_anchor,   # 定位在點的中心
                                                                               image=self.icon,           # 這裡沒有 load 圖片
                                                                               tag="marker")              # 這裡只是標注這個物件叫 marker
                        # 如果有指定命令，則綁定相應的事件
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.canvas_icon, "<Button-1>", self.click)
                    else:
                        # 更新圖像的位置, 就是如果已經創建了圖像則就只需要更新位置而已
                        self.map_widget.canvas.coords(self.canvas_icon, canvas_pos_x, canvas_pos_y)

                # draw standard icon shape
                # 如果沒有指定圖標，則繪製標準的標記形狀
                else: #圖標是由多邊形和圓形所構成
                    if self.polygon is None:
                        # 在畫布上創建多邊形並設置相關屬性
                        self.polygon = self.map_widget.canvas.create_polygon(canvas_pos_x - 14, canvas_pos_y - 23,
                                                                             canvas_pos_x, canvas_pos_y,
                                                                             canvas_pos_x + 14, canvas_pos_y - 23,
                                                                             fill=self.marker_color_outside, width=2,
                                                                             outline=self.marker_color_outside, tag="marker")
                        # 如果有指定命令，則綁定相應的事件
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.polygon, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.polygon, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.polygon, "<Button-1>", self.click)
                    else:
                        # 如果已經創建了圖標的多邊形則更新多邊形的位置
                        self.map_widget.canvas.coords(self.polygon,
                                                      canvas_pos_x - 14, canvas_pos_y - 23,
                                                      canvas_pos_x, canvas_pos_y,
                                                      canvas_pos_x + 14, canvas_pos_y - 23)
                    if self.big_circle is None:
                        # 在畫布上創建大圓形並設置相關屬性
                        self.big_circle = self.map_widget.canvas.create_oval(canvas_pos_x - 14, canvas_pos_y - 45,
                                                                             canvas_pos_x + 14, canvas_pos_y - 17,
                                                                             fill=self.marker_color_circle, width=6,
                                                                             outline=self.marker_color_outside, tag="marker")
                        # 如果有指定命令，則綁定相應的事件
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.big_circle, "<Button-1>", self.click)
                    else:
                        # 如果已經創建了圖標的圓形則更新大圓形的位置
                        self.map_widget.canvas.coords(self.big_circle,
                                                      canvas_pos_x - 14, canvas_pos_y - 45,
                                                      canvas_pos_x + 14, canvas_pos_y - 17)
                # 如果有指定文字，則繪製文字
                if self.text is not None:
                    if self.canvas_text is None:
                        # 在畫布上創建文字並設置相關屬性
                        self.canvas_text = self.map_widget.canvas.create_text(canvas_pos_x, canvas_pos_y + self.text_y_offset,
                                                                              anchor=tkinter.S,
                                                                              text=self.text,
                                                                              fill=self.text_color,
                                                                              font=self.font,
                                                                              tag=("marker", "marker_text"))
                        # 如果有指定命令，則綁定相應的事件
                        if self.command is not None:
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Enter>", self.mouse_enter)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Leave>", self.mouse_leave)
                            self.map_widget.canvas.tag_bind(self.canvas_text, "<Button-1>", self.click)
                    else:
                        # 更新文字的位置和內容
                        self.map_widget.canvas.coords(self.canvas_text, canvas_pos_x, canvas_pos_y + self.text_y_offset)
                        self.map_widget.canvas.itemconfig(self.canvas_text, text=self.text)
                else:
                    # 如果文字為空，則刪除已存在的文字
                    if self.canvas_text is not None:
                        self.map_widget.canvas.delete(self.canvas_text)
                # 如果有指定圖片且符合縮放可見性條件，則繪製圖片
                if self.image is not None and self.image_zoom_visibility[0] <= self.map_widget.zoom <= self.image_zoom_visibility[1]\
                        and not self.image_hidden:

                    if self.canvas_image is None:
                        # 在畫布上創建圖片並設置相關屬性
                        self.canvas_image = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30),
                                                                                anchor=tkinter.S,
                                                                                image=self.image,
                                                                                tag=("marker", "marker_image"))
                    else:
                        # 更新圖片的位置
                        self.map_widget.canvas.coords(self.canvas_image, canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30))
                else:
                    # 如果圖片不符合顯示條件，則刪除已存在的圖片
                    if self.canvas_image is not None:
                        self.map_widget.canvas.delete(self.canvas_image)
                        self.canvas_image = None
            else:
                # 如果標記不在畫布的可視範圍內，則刪除所有相關的畫布元素
                self.map_widget.canvas.delete(self.canvas_icon)
                self.map_widget.canvas.delete(self.canvas_text)
                self.map_widget.canvas.delete(self.polygon)
                self.map_widget.canvas.delete(self.big_circle)
                self.map_widget.canvas.delete(self.canvas_image)
                self.canvas_text, self.polygon, self.big_circle, self.canvas_image, self.canvas_icon = None, None, None, None, None

            self.map_widget.manage_z_order()
