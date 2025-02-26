import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene, 
                             QGraphicsRectItem, QGraphicsPathItem, QGraphicsTextItem, 
                             QAction, QMenu)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen, QPainterPath
import json

# 노드 클래스 (장면)
class SceneNode(QGraphicsRectItem):
    def __init__(self, node_id, text, x=0, y=0):
        super().__init__(0, 0, 150, 100)
        self.setPos(x, y)
        self.default_brush = QBrush(QColor(200, 200, 255))  # 기본 색상
        self.setBrush(self.default_brush)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        
        self.node_id = node_id
        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.text_item.setPos(10, 10)
        self.use_ai = False

    def mouseDoubleClickEvent(self, event):
        self.text_item.setFocus()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            menu = QMenu()
            delete_action = menu.addAction("삭제")
            use_ai_action = menu.addAction("AI 사용" if not self.use_ai else "AI 사용 해제")
            action = menu.exec_(event.screenPos())
            if action == delete_action:
                self.delete_item()
            elif action == use_ai_action:
                self.use_ai = not self.use_ai
                print(f"Node {self.node_id} use_ai: {self.use_ai}")
        super().mousePressEvent(event)

    def delete_item(self):
        for item in self.scene().items():
            if isinstance(item, ChoiceEdge) and (item.source == self or item.target == self):
                item.delete_item()
        self.scene().removeItem(self)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged:
            for item in self.scene().items():
                if isinstance(item, ChoiceEdge) and (item.source == self or item.target == self):
                    item.update_path()
        elif change == QGraphicsRectItem.ItemSelectedHasChanged:
            # 선택 상태에 따라 색상 변경
            if self.isSelected():
                selected_nodes = [item for item in self.scene().selectedItems() if isinstance(item, SceneNode)]
                if len(selected_nodes) == 1:
                    self.setBrush(QBrush(QColor(255, 200, 200)))  # 출발 노드: 연한 빨강
                elif len(selected_nodes) == 2 and selected_nodes[1] == self:
                    self.setBrush(QBrush(QColor(200, 255, 200)))  # 종착 노드: 연한 초록
            else:
                self.setBrush(self.default_brush)  # 선택 해제 시 기본 색상
        return super().itemChange(change, value)

# 엣지 클래스 (선택지)
class ChoiceEdge(QGraphicsPathItem):
    def __init__(self, source, target, choice_text, scene):
        super().__init__()
        self.source = source
        self.target = target
        self.scene_ref = scene
        self.setPen(QPen(QColor(0, 0, 0), 2))
        self.setZValue(-1)
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        
        self.label_item = QGraphicsTextItem(choice_text)
        self.label_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.scene_ref.addItem(self.label_item)
        self.update_path()

    def update_path(self):
        path = QPainterPath()
        start = self.source.pos() + self.source.boundingRect().center()
        end = self.target.pos() + self.target.boundingRect().center()
        
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        ctrl1 = start + QPointF(dx * 0.25, dy * 0.25)
        ctrl2 = start + QPointF(dx * 0.75, dy * 0.75)
        
        path.moveTo(start)
        path.cubicTo(ctrl1, ctrl2, end)
        
        arrow_size = 10
        p1 = path.pointAtPercent(0.99)
        p2 = path.pointAtPercent(1.0)
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            dx /= length
            dy /= length
        else:
            dx, dy = -1, 0
        
        tan30 = 0.577
        arrow_p2 = end - QPointF(dx * arrow_size - dy * arrow_size * tan30, dy * arrow_size + dx * arrow_size * tan30)
        arrow_p3 = end - QPointF(dx * arrow_size + dy * arrow_size * tan30, dy * arrow_size - dx * arrow_size * tan30)
        
        arrow_path = QPainterPath()
        arrow_path.moveTo(end)
        arrow_path.lineTo(arrow_p2)
        arrow_path.lineTo(arrow_p3)
        arrow_path.lineTo(end)
        path.addPath(arrow_path)
        
        self.setPath(path)
        
        mid_point = path.pointAtPercent(0.5)
        self.label_item.setPos(mid_point)

    def mouseDoubleClickEvent(self, event):
        self.label_item.setFocus()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            menu = QMenu()
            delete_action = menu.addAction("삭제")
            action = menu.exec_(event.screenPos())
            if action == delete_action:
                self.delete_item()
        super().mousePressEvent(event)

    def delete_item(self):
        try:
            if self.label_item.scene():
                self.scene_ref.removeItem(self.label_item)
            if self.scene():
                self.scene_ref.removeItem(self)
        except AttributeError as e:
            print(f"삭제 중 오류 발생: {e}")

# 메인 윈도우
class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Story Flowchart Editor")
        self.setGeometry(100, 100, 800, 600)
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        
        self.nodes = {}
        self.edges = []
        
        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("파일")
        edit_menu = menubar.addMenu("편집")

        new_action = QAction("새로 만들기", self)
        save_action = QAction("저장", self)
        export_action = QAction("게임 엔진용 내보내기", self)
        add_node_action = QAction("새 노드 추가", self)
        add_edge_action = QAction("선택지 추가", self)
        delete_action = QAction("선택된 항목 삭제", self)

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(export_action)
        edit_menu.addAction(add_node_action)
        edit_menu.addAction(add_edge_action)
        edit_menu.addAction(delete_action)

        new_action.triggered.connect(self.clear_editor)
        save_action.triggered.connect(self.save_to_json)
        export_action.triggered.connect(self.export_for_game)
        add_node_action.triggered.connect(self.add_node)
        add_edge_action.triggered.connect(self.add_edge)
        delete_action.triggered.connect(self.delete_selected_items)

    def add_node(self):
        node_id = f"node_{len(self.nodes)}"
        node = SceneNode(node_id, "새 장면", 100 + len(self.nodes) * 20, 100)
        self.scene.addItem(node)
        self.nodes[node_id] = node

    def add_edge(self):
        selected = [item for item in self.scene.selectedItems() if isinstance(item, SceneNode)]
        if len(selected) == 2:
            edge = ChoiceEdge(selected[0], selected[1], "새 선택지", self.scene)
            self.scene.addItem(edge)
            self.edges.append(edge)
            for node in selected:
                node.setSelected(False)  # 선택 해제 시 색상 복구를 위해

    def delete_selected_items(self):
        for item in self.scene.selectedItems():
            if isinstance(item, SceneNode):
                item.delete_item()
            elif isinstance(item, ChoiceEdge):
                item.delete_item()

    def clear_editor(self):
        self.scene.clear()
        self.nodes.clear()
        self.edges.clear()

    def save_to_json(self):
        self.nodes = {node.node_id: node for node in self.scene.items() if isinstance(node, SceneNode)}
        self.edges = [edge for edge in self.scene.items() if isinstance(edge, ChoiceEdge)]
        data = {"scenes": {}, "choices": []}
        
        for node_id, node in self.nodes.items():
            data["scenes"][node_id] = {
                "text": node.text_item.toPlainText(),
                "position": {"x": node.pos().x(), "y": node.pos().y()}
            }
        
        for edge in self.edges:
            data["choices"].append({
                "source": edge.source.node_id,
                "target": edge.target.node_id,
                "text": edge.label_item.toPlainText()
            })
        
        with open("test/edit_story.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("저장 완료: story.json")

    def export_for_game(self):
        self.nodes = {node.node_id: node for node in self.scene.items() if isinstance(node, SceneNode)}
        self.edges = [edge for edge in self.scene.items() if isinstance(edge, ChoiceEdge)]
        
        data = {"scenes": {}}
        
        for node_id, node in self.nodes.items():
            scene_data = {
                "text": node.text_item.toPlainText(),
                "choices": []
            }
            if node.use_ai:
                scene_data["use_ai"] = True
            data["scenes"][node_id] = scene_data
        
        for edge in self.edges:
            choice = {
                "text": edge.label_item.toPlainText(),
                "next_scene": edge.target.node_id
            }
            data["scenes"][edge.source.node_id]["choices"].append(choice)
        
        with open("test/story.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("내보내기 완료: game_story.json")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditorWindow()
    window.show()
    sys.exit(app.exec_())