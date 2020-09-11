import os
import tkinter
import tkinter.filedialog
import modules.calculator
import modules.contact
import modules.search
import modules.help_info
import SearchACT

__version__ = '1.0.0'

class SearchACTModel:
    def __init__(self, contact, searcher, calculator):
        self.contact = contact
        self.searcher = searcher
        self.calculator = calculator

    def search(self, text):
        try:
            matchIDs = self.searcher.parse_formula(text)
            if len(matchIDs) == 0:
                return [[f'\'{text}\' not found.']]
            else:
                data = []
                for matchID in matchIDs:
                    data.append(self.contact.DICT_KEY_CONTACT[matchID])
                return data
        except:
            return [['Formula error!']]

    def calculate(self, text):
        try:
            result = self.calculator.cal(text)
            return [[str(result)]]
        except:
            return [['Formula error!']]

    def updateContact(self, contact, searcher):
        self.contact = contact
        self.searcher = searcher

class ScrollTable(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [['Empty']]
        self.labels = []
        self.canvas = tkinter.Canvas(self)
        self.view = tkinter.Frame(self.canvas)
        self.vsb = tkinter.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.view, anchor='nw')
        self.canvas.bind('<Configure>', self.onCanvasConfigure)
        self.view.bind('<Configure>', self.onFrameConfigure)
        self.view.bind_all('<Button>', self.onMouseWheel)
        self.view.bind_all('<MouseWheel>', self.onMouseWheel)
        self.vsb.pack(side='right', fill='y')
        self.canvas.pack(fill='both', expand=True)
        self.update()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def onMouseWheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview('scroll', -1, 'units')
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview('scroll', 1, 'units')

    def update(self):
        for label in self.labels:
            label.grid_forget()
        self.labels = []
        for ridx, rdata in enumerate(self.data):
            for cidx, cdata in enumerate(rdata):
                label = tkinter.Label(self.view, text=cdata)
                label.grid(row=ridx, column=cidx, sticky='w')
                self.labels.append(label)

    def setData(self, data):
        self.data = data
        self.update()

class MessageWindow(tkinter.Toplevel):
    def __init__(self, text, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.minsize(200, 0)
        self.attributes('-topmost', 'true')
        self.messageBox = tkinter.Message(self, text=text, width=400)
        self.messageBox.pack(fill='both')
        self.bind('<Escape>', self.close)
        self.focus_force()
        self.grab_set()

    def close(self, *args, **kwargs):
        self.destroy()

class SearchACTView(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('SearchACT')
        self.geometry('800x600')
        self.mainMenu = tkinter.Menu(self)
        self.config(menu=self.mainMenu)
        self.fileMenu = tkinter.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.container = tkinter.Frame(self)
        self.container.pack(fill='both', padx=5, pady=5, expand=True)
        self.inputContainer = tkinter.Frame(self.container)
        self.inputContainer.pack(fill='x')
        self.inputLabel = tkinter.Label(self.inputContainer, text='Input:')
        self.inputText = tkinter.Entry(self.inputContainer)
        self.searchButton = tkinter.Button(self.inputContainer, text='Search')
        self.calculateButton = tkinter.Button(self.inputContainer, text='Calculate')
        self.inputLabel.pack(side='left')
        self.calculateButton.pack(side='right')
        self.searchButton.pack(side='right')
        self.inputText.pack(side='left', fill='x', expand=True)
        self.outputContainer = ScrollTable(self.container)
        self.outputContainer.pack(fill='both', expand=True)

    def openMsgWindow(self, text, title, *args, **kwargs):
        return MessageWindow(text, title, *args, **kwargs)

class SearchACTController:
    def __init__(self):
        self.rootPath = os.path.dirname(os.path.abspath(__file__))
        self.dataPath = os.path.join(self.rootPath, '_dict_key_contacts.pickle')
        self.dmapPath = os.path.join(self.rootPath, '_dict_terms_key.pickle')
        self.view = SearchACTView()
        [contact, search] = self.loadContact()
        cal = self.loadCalculator()
        self.model = SearchACTModel(contact, search, cal)
        self.view.searchButton['command'] = self.search
        self.view.calculateButton['command'] = self.calculate
        self.view.mainMenu.add_command(label='Info', command=self.info)
        self.view.fileMenu.add_command(label='Load', command=self.setContactFiles)
        self.view.inputText.focus_set()
        self.view.inputText.bind('<Return>', self.search)
        self.view.inputText.bind('<KP_Enter>', self.search)
        self.view.inputText.bind('<Control-Key-Return>', self.calculate)
        self.view.inputText.bind('<Control-Key-KP_Enter>', self.calculate)
        self.view.inputText.bind('<Control-KeyRelease-a>', self.selectAll)
        self.view.inputText.bind('<Control-KeyRelease-A>', self.selectAll)
        self.view.bind('<Control-Key-l>', self.setContactFiles)
        self.view.bind('<Control-Key-L>', self.setContactFiles)
        self.view.bind('<Control-Key-i>', self.info)
        self.view.bind('<Control-Key-I>', self.info)
        self.view.bind('<Double-Escape>', self.close)
        self.view.mainloop()

    def close(self, *args, **kwargs):
        self.view.destroy()

    def info(self, *args, **kwargs):
        mver = SearchACT.__version__
        gver = __version__
        text = f'Main version {mver}\nGUI version {gver}'
        self.view.openMsgWindow(text, 'Info')

    def setContactFiles(self, *args, **kwargs):
        dataPath = tkinter.filedialog.askopenfilename(
            title='Select a key contact file',
            initialdir=self.rootPath,
            filetypes=[('Pickle files', '.pickle')]
        )
        dmapPath = tkinter.filedialog.askopenfilename(
            title='Select a terms key file',
            initialdir=self.rootPath,
            filetypes=[('Pickle files', '.pickle')]
        )
        if all([type(dataPath) == str, type(dmapPath) == str]):
            self.dataPath = dataPath
            self.dmapPath = dmapPath
            [contact, search] = self.loadContact()
            self.model.updateContact(contact, search)

    def loadContact(self, *args, **kwargs):
        if all([os.path.isfile(self.dataPath), os.path.isfile(self.dmapPath)]):
            contact = modules.contact.Contact(self.dataPath, self.dmapPath)
            search = modules.search.SearchACT(contact.DICT_TERM_KEY)
            return [contact, search]
        else:
            self.view.openMsgWindow('No contact files', 'Error')
            return [None, None]

    def loadCalculator(self, *args, **kwargs):
        names = modules.calculator.names
        ops = modules.calculator.ops
        return modules.calculator.Calculator(names, ops)

    def selectAll(self, *args, **kwargs):
        self.view.inputText.select_range(0, tkinter.END)
        self.view.inputText.icursor(tkinter.END)

    def search(self, *args, **kwargs):
        text = self.view.inputText.get()
        result = self.model.search(text)
        self.view.outputContainer.setData(result)

    def calculate(self, *args, **kwargs):
        text = self.view.inputText.get()
        result = self.model.calculate(text)
        self.view.outputContainer.setData(result)

if __name__ == '__main__':
    app = SearchACTController()
