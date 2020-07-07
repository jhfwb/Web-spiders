import os
import time

from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError

from src.GYS_pySpiders import Action
from src.GYS_pySpiders.Action import Store

from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
from src.GYS_pySpiders.utils.RR_Comments import PrintTool


class Command(ScrapyCommand):
    requires_project = True
    def syntax(self):
        return "[options] <spider>"
    def short_desc(self):
        return "Run a spider"
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output:
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            valid_output_formats = feed_exporters.keys()
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')
    def run(self, args, opts):
        # 获取爬虫列表
        # spd_loader_list = self.crawler_process.spider_loader.list()  # 获取所有的爬虫文件。
        # 获取config.xml中的爬虫信息。
        actionConfigUtils=Store.take("actionConfigUtils",SpidersConfigUitls())
        for spname in actionConfigUtils.execs:
            self.crawler_process.crawl(spname['webName'], **opts.spargs)


        # for spname in spd_loader_list or args:
        #     #运行第一次爬虫
        #     # configUtils=Store.get(spname)
        #     # opts.spargs.setdefault(spname,configUtils)#给spider传递参数
        #     self.crawler_process.crawl(spname, **opts.spargs)

        self.crawler_process.start()
        # self.crawler_process.start()

