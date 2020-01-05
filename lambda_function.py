import os
import linebot_publisher
import yahoo_tv_search.src.yahoo_tv_search as ytv


KEYWORD = '北海道'
MAX_TITLE_LEN = 20
LINE_BOT_TO_ID = os.environ.get('LINE_BOT_TO_ID')


def lambda_handler(event={}, context={}):
    tv_searcher = ytv.Searcher()
    tv_programs = tv_searcher.run(
        keyword=KEYWORD,
        broad_types=[
            ytv.SearchOption.Broadcast.TERRESTRIAL,
            ytv.SearchOption.Broadcast.BS,
        ]
    )

    message = ''
    old_date = ''
    publisher = linebot_publisher.LineBotPublisher()
    publisher.post_text(LINE_BOT_TO_ID, '{} の番組だよ'.format(KEYWORD))

    for prog in tv_programs:
        if prog.date != old_date:
            message += '{date}\n'.format(date=prog.date)
            old_date = prog.date

        format_title = '{title}{ellipsis}'.format(
            title=prog.title[:MAX_TITLE_LEN],
            ellipsis='...' if len(prog.title) > MAX_TITLE_LEN else ''
        )
        message += '{time} {title} [{channel}]\n'.format(
            time=prog.time,
            title=format_title,
            channel=prog.channel
        )

        if len(message) > publisher.MAX_TEXT_LENGTH - 100:
            publisher.post_text(
                LINE_BOT_TO_ID,
                message
            )
            message = ''


if __name__ == '__main__':
    lambda_handler()
