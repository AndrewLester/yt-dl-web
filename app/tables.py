from flask_table import Table, Col, ButtonCol
from pytube import YouTube, itags, streams
import urllib.request
class ItemTable(Table):
    classes = ["table"]
    itag = Col('itag')
    res = Col('Resolution')
    bitrate = Col('bitrate')
    size = Col('size')
    button = ButtonCol('Download', endpoint="download",
    button_attrs={'id': 'dl_button','onclick':'update_form_info(this)'}, form_attrs={'action': ''},
    form_hidden_fields={'itag':'temp_itag'})

class Item(object):
    def __init__(self, itag, res, bitrate, size):
        self.itag = itag
        self.res = res
        self.bitrate = bitrate
        self.size = size

class Table():
    def __init__(self, link):
        self.link=link
        self.yt = YouTube(self.link)
        self.items = []

    def fill_table(self):
        self.itag_list = self.yt.get_itag_list()
        self.itag_list.sort()
        print(self.itag_list, "before")
        for x in self.itag_list:
            print(x, "index")
            try:
                urllib.request.urlopen(self.yt.streams.get_by_itag(x).url)
                # pytube for sometimes gives streams that dont exist, this doesn't allow them through
            except:
                # self.itag_list.remove(x) - for some reason this doesnt work
                print(x, "FAILED!")
                continue
            else:
                print(x,"continuing")
                self.items.append(
                    Item(
                        x,
                        itags.get_format_profile(x)['resolution'],
                        itags.get_format_profile(x)['abr'],
                        str(self.yt.streams.get_by_itag(x).filesize_approx/1000000) + " MB" # sizes are NOT accurate, only estimates
                    )
                )
        print(self.itag_list, "after")
    def return_table(self):
        table = ItemTable(self.items)
        return table
