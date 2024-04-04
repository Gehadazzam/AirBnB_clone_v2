#  we’d like you to install and configure an Nginx server using Puppet instead of Bash
# Update system before installing nginx
exec { 'install_system':
    command => '/usr/bin/apt-get update',
}

# Install Nginx
package { 'nginx':
    ensure  => 'installed',
    require => Exec['install_system']
}

# Ensure Nginx service is running
service {'nginx':
    ensure  => running,
    require => Package['nginx']
}

# Create necessary directories
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

# Create index.html file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Hello kitty! How are you.xoxoxo\n"
} ->

# Create a symbolic link to the test directory
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

# Change ownership of /data directory
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Update Nginx configuration to serve content to hbnb_static
file { '/etc/nginx/sites-available/kitty401984':
  ensure  => 'present',
  content => "
    server {
        listen 80;
        server_name kitty401984;

        location / {
            root /data/web_static/current/;
            index index.html index.htm;
        }

        location /hbnb_static/ {
            alias /data/web_static/current/;
            index index.html index.htm;
        }
    }
  ",
  require => Package['nginx'],
  notify  => Exec['nginx_run'],
}

# Enable the new site by creating a symbolic link
file { '/etc/nginx/sites-enabled/kitty401984':
  ensure  => 'link',
  target  => '/etc/nginx/sites-available/kitty401984',
  require => File['/etc/nginx/sites-available/kitty401984'],
  notify  => Exec['nginx_run'],
}

# Restart Nginx service after updating the configuration
exec {'nginx_run':
    command => '/usr/sbin/service nginx restart',
    refreshonly => true,
}
