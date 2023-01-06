import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class SetUi():   
    def __init__(self, form):
        self._translate = QtCore.QCoreApplication.translate
        form.setObjectName("form")
        form.resize(400, 600)
        self.grid_layout_widget = QtWidgets.QWidget(form)
        self.grid_layout_widget.setGeometry(QtCore.QRect(9, 79, 381, 511))
        self.grid_layout_widget.setObjectName("grid_layout_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("gridLayout")
        self.buttons_on_grid()
        self.display(form)
        form.setWindowTitle(self._translate("form", "Custom Calc"))
        QtCore.QMetaObject.connectSlotsByName(form)

    def buttons_on_grid(self):
        self.button_instance('C', 0, 2)
        self.button_instance('=', 0, 3)
        
        self.button_instance('7', 1, 0)
        self.button_instance('8', 1, 1)
        self.button_instance('9', 1, 2)
        self.button_instance('/', 1, 3)
        
        self.button_instance('4', 2, 0)
        self.button_instance('5', 2, 1)
        self.button_instance('6', 2, 2)
        self.button_instance('*', 2, 3)

        self.button_instance('1', 3, 0)
        self.button_instance('2', 3, 1)
        self.button_instance('3', 3, 2)
        self.button_instance('-', 3, 3)

        self.button_instance('Del', 4, 0)
        self.button_instance('0', 4, 1)
        self.button_instance('.', 4, 2)
        self.button_instance('+', 4, 3)

    def button_instance(self, txt, n0, n1):
        self.tool_button = QtWidgets.QToolButton(self.grid_layout_widget)
        self.tool_button.setMinimumSize(QtCore.QSize(80, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.tool_button.setFont(font)
        self.tool_button.setText(self._translate("form", txt))
        self.tool_button.setObjectName(txt)
        self.grid_layout.addWidget(self.tool_button, n0, n1, 1, 1)
        self.tool_button.clicked.connect(lambda: self.throw_txt(txt))
        
    def throw_txt(self, txt):
        calc = Calc()
        temp = self.line_edit.text()
        answer = calc.ch_Main(txt, temp)
        self.line_edit.setText(answer)
        
    def display(self, form):
        self.line_edit = QtWidgets.QLineEdit(form)
        self.line_edit.setObjectName("lineEdit")
        self.line_edit.setGeometry(QtCore.QRect(10, 10, 381, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.line_edit.setFont(font)
        self.line_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.line_edit.setDragEnabled(False)
        self.line_edit.setReadOnly(True)
        self.line_edit.setClearButtonEnabled(False)
        self.line_edit.setText(QtCore.QCoreApplication.translate("form", u"0", None))

class Calc():
    operator = ['+','-','*','/','.','=']
    def __init__(self):
        pass

    def ch_Main(self, txt, answer):
        f = Functions()
        answer = f.reset_answer_tryagain(txt, answer)
        if txt == 'Del':
            answer = f.delete(answer)
        elif txt == 'C':
            answer = f.clear(answer)
        elif txt == '=':
            if answer == '0':
                answer = '0'
            elif len(answer) == 1 and answer not in Calc.operator:
                answer = answer
            elif answer[-1] in Calc.operator:
                answer = f.delete(answer)                
            else:
                answer = self.calculator(txt, answer)
        else:
            answer += txt
            answer = f.remove_twice_operator(txt, answer)
            answer = f.remove_first_zero(answer)
            answer = f.zero_zero(txt, answer)
        return answer

    def calculator(self, txt, answer):
        f = Functions()
        answer = f.remove_first_zero(answer)
        answer = f.zero_division_error(answer)        
        answer = eval(answer)
        answer = str(answer)
        answer = f.check_lastdot_zero(answer)
        answer = f.zero_zero(txt, answer)
        return answer


class Functions:
    txtlist = ''

    def __init__(self):
        pass

    def delete(self, temp):
        temp = temp[:-1]
        if temp == '':
            temp = '0'
        return temp        

    def clear(self, temp):
        temp = '0'
        return temp

    def remove_twice_operator(self, txt, answer):
        if len(answer)>1:
            if answer[-2] in Calc.operator and answer[-1] in Calc.operator:
                answer = answer[:-2] + txt
        return answer

    def reset_answer_tryagain(self, txt, answer):
        Functions.txtlist += txt
        if len(Functions.txtlist)>1:
            if Functions.txtlist[-2] == '=' and Functions.txtlist[-1] not in Calc.operator:
                answer = '0'
                Functions.txtlist = ''
        return answer

    def zero_division_error(self, answer):
        if answer[-2] == '/' and answer[-1] =='0':
            answer = '0'
        return answer

    def zero_zero(self, txt, answer):
        if txt == '0' and answer == '0':
            answer = '0'
        elif txt == '0' and answer == '':
            answer = '0'
        elif answer == '':
            answer = '0'
        return answer
    
    def remove_first_zero(self, answer):
        if answer[0] == '0':
            if len(answer) > 0 and answer[1] == '.':
                pass
            elif len(answer) > 0 and answer[1] not in Calc.operator:
                answer = answer.lstrip('0')
        else:
            pass
        return answer

    def check_lastdot_zero(self, ans):
        ans = ans.rstrip(".0")
        return ans

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = SetUi(form)
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()