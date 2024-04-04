# Redo the task #0 but by using Puppet

# Setup web servers for deployment of web_static

# Install nginx if not already installed
package { 'nginx':
  ensure => installed,
}

# Create directories if they don't exist
file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Hello kitty! How are you.xoxox\n",
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Give ownership of /data/ folder to the ubuntu user and group
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update nginx configuration to serve content
file_line { 'nginx_hbnb_static':
  ensure => present,
  path   => '/etc/nginx/sites-available/default',
  line   => '    location /hbnb_static/ { alias /data/web_static/current/; }',
}

# Restart nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File_line['nginx_hbnb_static'],
}
