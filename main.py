from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.clock import Clock
import chess
import minmax
import time

class ChessBoard(Widget):
    menu_widget = ObjectProperty()
    def __init__(self, **kwargs):
        super(ChessBoard, self).__init__(**kwargs)
        self.piece_imgs = {
            'p': 'bp.png',
            'n': 'bn.png',
            'b': 'bb.png',
            'r': 'br.png',
            'q': 'bq.png',
            'k': 'bk.png',
            'P': 'wp.png',
            'B': 'wb.png',
            'N': 'wn.png',
            'R': 'wr.png',
            'Q': 'wq.png',
            'K': 'wk.png'
        }
        self.dragging_piece = None
        self.dragging_pos = (0, 0)
        self.piece_from = None
        self.draw_board()
        self.load_pieces()
        
  

    def draw_board(self):
        # self.canvas.clear()
        board_size = min(self.width, self.height)
        square_size = board_size / 8      
        with self.canvas:
            for row in range(8):
                for col in range(8):
                    color = (.3, .6, 0, 1) if (row + col) % 2 == 0 else (.9, 1, .91, 1)
                    Color(*color)
                    Rectangle(pos=(col * square_size, row * square_size), size=(square_size, square_size))
                    
    def load_pieces(self):
        board_size = min(self.width, self.height)
        square_size = board_size / 8 

        for widget in list(self.children):
            if isinstance(widget, Image):
                self.remove_widget(widget)
        
        for row in range(8):
            for col in range(8):
                square = chr(97+col) + str(8-row)
                parsed_square = chess.parse_square(square)
                piece_det = board.piece_at(parsed_square)
                if piece_det is not None:
                    piece = piece_det.symbol()
                    img = Image( source=self.piece_imgs[piece], size=(square_size, square_size), pos=((col)*square_size, (7-row)*square_size))
                    self.add_widget(img)
    
    def on_touch_down(self, touch):
        board_size = min(self.width, self.height)
        square_size = board_size / 8

        if self.collide_point(*touch.pos):
            for widget in self.children:
                if isinstance(widget, Image):
                    if widget.collide_point(*touch.pos):
                        self.dragging_piece = widget
                        self.dragging_pos = touch.pos

                        col = int(touch.x / square_size)
                        row = int(touch.y / square_size)

                        self.piece_from = chr(97 + col) + str(row+1)
                        return True
        return super(ChessBoard, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging_piece:
            # Move the piece with the touch
            if self.dragging_piece.collide_point(*touch.pos):
                self.dragging_piece.pos = (touch.x - self.dragging_piece.width / 2,
                                           touch.y - self.dragging_piece.height / 2)
            return True
        return super(ChessBoard, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragging_piece:
            board_size = min(self.width, self.height)
            square_size = board_size / 8
            
            col = int(touch.x / square_size)
            row = int(touch.y / square_size)
            col = max(0, min(7, col))
            row = max(0, min(7, row))
            
            new_x = col * square_size
            new_y = row * square_size

            piece_to = chr(97 + col) + str(row+1)
            move = self.piece_from + piece_to
            
            self.dragging_piece.pos = (new_x, new_y)
            self.dragging_piece = None

            try:
                if(current_player == chess.WHITE):
                    board.push_uci(move)
            except ValueError:
                self.load_pieces()
                return
            move = self.AI() 
            if move is not None:   
                board.push(move)
                self.load_pieces()
            else:
                self.load_pieces()

            if board.is_game_over():
                result = board.result()
                board.reset()
                time.sleep(3)
                
                if result == "1-0":
                    result = "White won!"
                elif result == "0-1":
                    result = "Black won!"
                else:
                    result = "Stalemate!"
                sm = self.parent.parent.parent.parent
                bid = sm.get_screen('main').ids.buttonID
                bid.text = 'Restart'
                lid = sm.get_screen('main').ids.labelID
                lid.text = result
                
                Clock.schedule_once(lambda dt: self.display_result(), 5)
                
                #sm.current = 'main'
                
               
            return True

        return super(ChessBoard, self).on_touch_up(touch)
       
    def display_result(self):
        self.parent.parent.parent.parent.current = 'main'
        self.load_pieces()
    
     
    def AI(self):
        best_move = None
        best_value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            board_value = minmax.minmax(board, depth, float('-inf'), float('inf'), False)
            board.pop()
            
            print(move, ': ', board_value)
        
            if best_value < board_value:
                best_value = board_value
                best_move = move
        print('The move picked: ', best_move, ' to ', best_value, '\n\n')
        return best_move


    def on_size(self, *args):
        self.draw_board()
        self.load_pieces()


class GamePlay(Screen):
    menu_title = StringProperty('C h e s s')
    menu_button_title = StringProperty('Start Game')
    menu_widget = ObjectProperty()
    def __init__(self, **kwargs):
        super(GamePlay, self).__init__(**kwargs)
        def on_enter(self, *args):
            menu_widget = self.manager.get_screen('main').ids.menu_widget
            chess_board = self.ids.chess_board 
            chess_board.menu_widget = menu_widget
        
    def on_option_click(self):
        pass
        
    def on_back_click(self):
        if init_board.fen() != board.fen():
            move = board.pop()
            prev_moves.append(move.uci())
            chess_board = self.ids.chess_board
            chess_board.load_pieces()
       
    def on_front_click(self):
        print(prev_moves)
        if prev_moves:
            move = prev_moves.pop()
            board.push_uci(move)
            chess_board = self.ids.chess_board
            chess_board.load_pieces() 
        

class CustomLayout(RelativeLayout):
    pass
    
class MenuWidget(Screen):
    pass
    
class MainApp(App):
    def build(self):
        #Builder.load_file('main.kv')
        sm = ScreenManager()
        sm.add_widget(MenuWidget(name='main'))
        sm.add_widget(GamePlay(name='second'))
        
        return sm
    
if __name__ == '__main__':
    board = chess.Board()
    init_board = chess.Board()
    prev_moves = []
    depth = 2
    current_player = board.turn
    MainApp().run()