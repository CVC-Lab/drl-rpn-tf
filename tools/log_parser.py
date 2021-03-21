import os
import argparse
import re

def main(args):
    line1_regex = re.compile(r'^iter: (?P<iter>\d{1,10}) \/ \d{1,10}, total loss: (?P<tot_loss>\d{1,10}.\d{1,10})')
    line2_regex = re.compile(r'^ >>> loss_cls \(detector\)\: (?P<loss_cls>\d{1,10}.\d{1,10})')
    line3_regex = re.compile(r'^ >>> loss_box \(detector\)\: (?P<loss_box>\d{1,10}.\d{1,10})')
    with open(args.output, "w") as out_file:
        out_file.write("iter tot_loss loss_cls loss_box\n")
        with open(args.input, "r") as in_file:
            line_index = 0
            iter, tot_loss, loss_cls, loss_box = 0, 0, 0, 0
            for line in in_file:
                if line_index == 0:
                    m = line1_regex.match(line)
                    if m:
                        iter = m.groupdict()['iter']
                        tot_loss = m.groupdict()['tot_loss']
                        line_index += 1
                    else:
                        line_index = 0
                elif line_index == 1:
                    m = line2_regex.match(line)
                    if m:
                        loss_cls = m.groupdict()['loss_cls']
                        line_index += 1
                    else:
                        line_index = 0
                elif line_index == 2:
                    m = line3_regex.match(line)
                    if m:
                        loss_box = m.groupdict()['loss_box']
                        out_file.write("%s %s %s %s\n" % (iter, tot_loss,
                                                          loss_cls, loss_box))
                    line_index = 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse DRL_RPN output')
    parser.add_argument('-i', '--input', default=None, type=str,
                        help='input log file')
    parser.add_argument('-o', '--output', default=None, type=str,
                        help='output as $iter $tot_loss $loss_cls $loss_box')


    main(parser.parse_args())