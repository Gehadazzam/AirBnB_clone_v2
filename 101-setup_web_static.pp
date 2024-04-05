# Redo the task #0 but by using Puppet:

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
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Install Nginx package
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Ensure directory structure for web_static
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

# Create a sample index.html file for /data/web_static/releases/test/
-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "webpage is found in data/web_static/releases/test/index.htm \n"
}

# Create a symbolic link /data/web_static/current
-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

# Change ownership of /data/ to ubuntu user and group
-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Ensure directory structure for /var/www/html
file { '/var/www':
  ensure => 'directory'
}

-> file { '/var/www/html':
  ensure => 'directory'
}

# Create index.html and 404.html in /var/www/html
-> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "upload in /var/www/index.html***\n"
}

-> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
}

# Update Nginx configuration with $nginx_conf
-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
}

# Restart Nginx service
-> exec { 'nginx restart':
  path => '/etc/init.d/'
}
