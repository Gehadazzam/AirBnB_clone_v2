#  we’d like you to install and configure an Nginx server using Puppet instead of Bash
#update before install nijinx
exec { 'install_system':
    command => '/usr/bin/apt-get update',
}
#install nignix
package { 'nginx':
    ensure  => 'installed',
    require => Exec['install_system']
}
#print hello world
file {'/var/www/html/index.html':
    content => 'Hello World!'
}
#handle redirect
exec {'redirect':
    command  => 'sed -i "24i\	rewrite ^/redirect https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;" /etc/nginx/sites-available/default',
    provider => 'shell'
}

service {'nginx':
    ensure  => running,
    require => Package['nginx']
}
file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Hello kitty! How are you.xoxoxo\n"
} ->
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

