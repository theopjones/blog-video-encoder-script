[GoBlog](https://goblog.app/) is a blogging engine that I have used on my personal blog, and various other personal projects. I'm going to do a walkthrough of how to set this up on a FreeBSD server.    

If you want a quick TLDR, here is a shell script that automatically spins up GoBlog. It doesn't set up a jail or other container, but it can be used in one.

https://gist.github.com/theopjones/e09c9713c10f4000d154de50c438d2ba

Its a blogging engine with fairly few users, and I wouldn't recommend it for important business websites, or people who aren't at least somewhat technically oriented and who know their way around UNIX-like operating systems.

But for the technically inclined, it makes a good personal blog. It is very performant and supports a lot of interesting social features, including most of the IndieWeb standards. It can also (with some limitations), talk to Mastedon and other similar ActivityPub using services, and allow these social services to subscribe to your blog.  

I previously had my personal blog on a Debian home server, using Docker for containerization.

I've discussed an overview of this setup here 

https://theopjones.blog/notes/2022/09/2022-09-12-oxjfr

https://theopjones.blog/posts/2022/09/2022-09-17-exlan

Unfortunately, my new apartment doesn't have any internet with the fast upload speeds needed for this type of home server setup, so I'm moving my setup to a dedicated server. 

I've decided to go with FreeBSD for this setup because it has a lot of powerful features, and in my opinion is a often lot more streamlined and elegant than Linux in how it handles things.

I'd recommend spinning up a jail to act as a container to separate this setup from the rest of your system, particularly if you want to run more than one service on your server/VPS. 

In the future, I'll write up instructions and a shell script on how to build this in a jail and set up a reverse proxy with SSL for this (either Caddy or Nginx would make a good fit for reverse proxy). 

There are multiple helper tools to set this up. I like [BastilleBSD](https://bastillebsd.org/) for this role. 

Likely because it is a small blogging engine without very many users, there isn't a FreeBSD port or package for this, so, we will need to compile it from the Git repo. 

We will need the following FreeBSD packages to do this `go-devel git gcc sqlite3 bash`

GoBlog can also use `tor` for creating a .onion service for site visitors who want additional privacy when viewing your blog. 

I have created a Python script (discussed later) to help with generating a config file, if you want to use that, you will also need `python3 py39-yaml`.

See the following command for how to install all of these packages 

`pkg install go-devel git gcc sqlite3 bash tor python3 py39-yaml`

To clone the Goblog source code from Git, run the following command

`git clone https://github.com/jlelse/GoBlog.git`

Change directory into the newly downloaded source code repo.

`cd GoBlog`

Build the GoBlog source code

`go-devel build -tags=sqlite_fts5 -ldflags '-w -s' -o GoBlog`

Copy GoBlog to `/usr/local/bin/` (the appropriate folder given standard FreeBSD folder structure. Give the Goblog executable the right permissions to be ran by all users. 

install -m 755 GoBlog /usr/local/bin/GoBlog

The data directory that our RC script (more details later in this post) will use as the working directory is `/var/GoBlog/`

Additional data used by Goblog is contained in the following folders in the Git repo `pkgs testdata templates leaflet hlsjs dbmigrations strings plugins`

Create a corresponding folder for each of these under `/var/GoBlog/` and copy the contents. 

Create empty folders `/var/GoBlog/data` and `/var/GoBlog/config. This is for user generated data which persists across versions. The `data` folder will be populated on the first run of GoBlog.

The config file will need to be manually generated. An example config file is contained in the GoBlog git repo as `example-config.yml`.  

You can also use the following python script I have created to guide you through the process of creating the config file. It will prompt you for the information needed to set up the most common configurations. 

https://gist.github.com/theopjones/748c296b3c33881352bb7ac72772ae67

Next up we will need to create an RC file for GoBlog. I have created one as follows

https://gist.github.com/theopjones/d62e480a71f5cbcead7e381ffd422fda

(Both of the above scripts are created and used by the whole installation shell script mentioned at the beginning of the post.

Write it to `/usr/local/etc/rc.d/goblog`

Then make the rc script file executable

`chmod +x "$rc_script_file"`

Enable GoBlog to load when the system does 

`echo 'goblog_enable="YES"' >> /etc/rc.conf`
