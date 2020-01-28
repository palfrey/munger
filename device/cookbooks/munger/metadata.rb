name             'munger'
maintainer       'Tom Parker-Shemilt'
maintainer_email 'palfrey@tevp.net'
license          'AGPL-3.0-only'
description      'Cloud scanner'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.1.0'
source_url       'https://github.com/palfrey/munger'
issues_url       'https://github.com/palfrey/munger/issues'
chef_version     '>=13'

depends 'line'
supports 'debian'