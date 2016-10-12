from argparse import ArgumentParser
import datetime
import calendar
from lxml import etree
from lxml.etree import HTMLParser
from os import system
    
def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--test", help="test mode, just print commands", default=False, action='store_true')
    parser.add_argument("-d", "--date", help="override date <YYYY-MM-DD DDD>", default=None)
    parser.add_argument("-f", "--file", help="input file", default="index.html")
    parser.add_argument("-n", "--ncopies", help="number of copies", default=1, type=int)
    parser.add_argument("-s", "--scan", help="scan column", default=2, type=int)
    parser.add_argument("-c", "--column", help="target column index", default=4, type=int)
    parser.add_argument("-i", "--id", help="table id", default="orgtable1")
    options = vars(parser.parse_args())

    today = datetime.date.today().strftime("<%Y-%m-%d %a>")
    if options['date'] is not None:
        today = options['date']
    print("searching for %s" % today)

    index_file = open(options['file'], "r")
    parser = HTMLParser()
    index_tree = etree.parse(index_file, parser)

    try:
        today_row = index_tree.xpath("//table[@id='%s']//td[%d]/span/span[contains(text(), '%s')]/../../.." % (options['id'], options['scan'], today))[0]
    except:
        print("not found")
        exit(0)

    link_targets = today_row.xpath("td[%s]/a/@href" % options['column'])
    for link_target in link_targets:
        if (not link_target.endswith(".pdf")) or link_target.startswith("http"):
            continue
        command = "lp -n %d %s" % (options['ncopies'], link_target)
        print(command)
        if options['test']:
            continue
        system(command)

if __name__=='__main__':
    main()
