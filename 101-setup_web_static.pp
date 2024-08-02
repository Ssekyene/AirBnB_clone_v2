# Setting up web servers for deployment with puppet

$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://www.google.com;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "<html>\n\t<head>\n\t\t<title>Holberton</title>\n\t</head> \
\n\t<body>\n\t\t<h1>Holberton Says Hello!</h1>\n\t</body>\n</html>"
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec { 'chown -hR ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

file { '/var/www':
  ensure => 'directory'
}

-> file { '/var/www/html':
  ensure => 'directory'
}

-> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "<body>Hello World</body>"
}

-> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page - Error page\n"
}

-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
}

-> exec { 'nginx restart':
  path => '/etc/init.d/'
}
