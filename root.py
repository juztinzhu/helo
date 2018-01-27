import web
import pymysql
import fileMgr

render = web.template.render('templates/', base='layout',
                             globals={'hasattr': hasattr})

urls = (
    '/', 'Index',
    '/view/(.*)', 'View',
    '/manage', 'Manage',
    '/manage/create', 'Create',
    '/manage/hide/(\d+)', 'Hide',
    '/manage/show/(\d+)', 'Show',
    '/manage/edit/(\d+)', 'Edit',
    '/fileop', 'fileMgr.FileMgr'
)


con = pymysql.connections.Connection(host='localhost',
                                     user='webuser',
                                     database='heli',
                                     autocommit=True,
                                     charset='utf8')
con.connect()
cur = pymysql.cursors.DictCursor(con)


def get_posts():
    cur.execute("select * from posts;")
    return cur.fetchall()


def get_post(id):
    cur.execute("select * from posts where id=%s;" % (id))
    return cur.fetchone()


def add_post(title, content):
    cur.execute("""insert into posts(title, content, hidden)
values('%s', '%s', 0);""" % (title, content))



def set_post(id, title, content):
    cur.execute("update posts set title='%s', content='%s', hidden=0 where id=%s;" % (title, content, id))


def hide_post(id):
    cur.execute("update posts set hidden=1 where id=%s;" % (id))
    return


def show_post(id):
    cur.execute("update posts set hidden=0 where id=%s;" % (id))
    return


class Index:
    def GET(self):
        posts = get_posts()
        return render.index(posts)


class View:
    def GET(self, id):
        content = get_post(id)
        return render.article(content)


class Manage:
    def GET(self):
        return render.manage(get_posts())


class Create:
    def GET(self):
        return render.edit({})

    def POST(self):
        input = web.input()
        # print(input)
        add_post(input.title, input.content)
        raise web.seeother("/manage")


class Edit:
    def GET(self, id):
        return render.edit(get_post(id))

    def POST(self, id):
        input = web.input()
        # print(input)
        set_post(id, input.title, input.content)
        raise web.seeother("/manage")


class Hide:
    def POST(self, id):
        hide_post(id)
        raise web.seeother("/manage")


class Show:
    def POST(self, id):
        show_post(id)
        raise web.seeother("/manage")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
