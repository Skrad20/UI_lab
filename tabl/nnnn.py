

    def fill_table_aus_base(self):
        """"""
        self.table_widget.clear()
        bus = MSSearchFater(
            name = 'ssdsd',
            BM1818 = '185/967',
        )


        labels = ['name', 'BM1818']

        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        with sqlite3.connect('db.sqlite3') as connect:
            for id_, name, price in connect.execute("SELECT id, name, price FROM Game WHERE kind = 'Finished'"):
                row = self.table_widget.rowCount()
                self.table_widget.setRowCount(row + 1)

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(id_)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(name))
                    self.table_widget.setItem(row, 2, QTableWidgetItem(price))
    