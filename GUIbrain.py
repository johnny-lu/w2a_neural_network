#!/usr/bin/env python
from gi.repository import Gtk
from keras.models import Sequential, load_model, Model
from pandas import read_csv
from datetime import datetime
import pandas
import numpy
import MySQLdb


class MainWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Parcel Prediction GUI v.0.1")
        self.set_border_width(10)
        self.set_size_request(200,100)
        #self.database = read_csv('unfinished_transactions.csv', header = 0, index_col='tid')
        self.database = db = MySQLdb.connect(user="root",passwd="w2a88888",db="test620",charset = 'utf8')
        self.cursor = self.database.cursor()
        self.timestamps = read_csv('time_stamps.csv', header = 0, index_col = 0)
    
        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # instructions label
        label = Gtk.Label()
        label.set_label("Enter parcel numbers here:")
        vbox.pack_start(label, True, True, 0)
        
        # tid entry box
        self.tids = Gtk.Entry()
        self.tids.set_text("TID1,TID2,TID3...")
        vbox.pack_start(self.tids, True, True, 0)

        # predict button
        predict_button = Gtk.Button(label="Predict")
        predict_button.connect("clicked", self.predict_clicked)
        vbox.pack_start(predict_button, True, True, 0)

        self.set_size_request(250,150)

    def get_information(self, tids):
        astr = ''
        for tid in tids:
            astr += str(tid) + ','
        astr = astr[:-1]
        command = 'SELECT tid, pay_consign, consign_scinbound, scinbound_lhdepart, lhdepart_lharrive, lharrive_ccout, ccout_signed from travel_time where tid in(%s)' % astr
        self.cursor.execute(command)
        full_info = self.cursor.fetchall()
        return full_info
        """ csv solution
        full_info = pandas.DataFrame()
        for tid in tids:
            full_info = full_info.append(self.database.loc[tid])
        return full_info
        """ 

    def predict_clicked(self, widget):
        nnInput = []
        tidList = self.tids.get_text()
        for i in tidList.split(', '):
            assert i.isdigit()
            nnInput.append(int(i)) 
        print nnInput
        fullInput = self.get_information(nnInput)
        processedInput = self.process_information(fullInput) 
        #self.legs(processedInput)      
        self.prediction(processedInput)
            
    def legs(self, processedInput):
        STATUSES = ['to consign', 'to scinbound', 'to lhdepart','to lharrive', 'to ccout', 'to signed']     
        counter = 0
        for i in processedInput:
            print STATUSES[counter]
            print('------------------------------------------')
            for j in i:
                print str(j[0]) + ',',
            counter += 1
            print ''
            

    def process_information(self, inputList): 
        status_lists = [[],[],[],[],[],[]]
        for i in inputList:
            counter = 1
            for j in i:
                if j == None:
                    status_lists[counter-2].append(i[:counter])
                    break
                counter += 1                
        return status_lists
                    
        """csv solution
        STATUSES = ['pay_consign', 'consign_scinbound', 'scinbound_lhdepart','lhdepart_lharrive', 'lharrive_ccout', 'total_time']
        status_lists = [[],[],[],[],[],[]]
        for index, row in anInput.iterrows():
            counter = 0
            for column in STATUSES:
                print row
                if numpy.isnan(row[column]):
                    status_lists[counter].append(row[column])
                    break
                counter = counter + 1
        return status_lists
        """

    def prediction(self, status_list):
        STATUSES = ['pay', 'consign', 'scinbound', 'lhdepart', 'lharrive', 'ccout']        
        count = 1
        for i in status_list:   
            alist = list()
            corr = list()            
            past_status = STATUSES[count-1]
            pcol = self.timestamps[past_status]
            
            for j in i:
                corr.append(j[0])
                appender = list(j[1:-1])
                dateee = datetime.strptime(pcol.loc[j[0]], '%Y-%m-%d %H:%M:%S')
                appender.append((datetime.now() - dateee).total_seconds())
                alist.append(appender)
                          
            count2 = 0
            if len(alist) > 0:
                try:
                    filename = 'my_model%s' % count            
                    modelx = load_model(filename)
                    predict = modelx.predict(alist)
                    for ans in predict.tolist():
                        print str(corr[count2]) + ': ',
                        ind = ans.index(max(ans))
                        if ind == 0:
                            print 'very late'
                        elif ind == 1:
                            print 'sort late'
                        elif ind == 2:
                            print 'not really late'
                        else:      
                            print 'not late'
                        count2 += 1
                except:
                    print 'is this model6'
            else:
                pass
            count += 1
         
            

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.set_position(Gtk.WindowPosition.CENTER)
window.show_all()
Gtk.main()
