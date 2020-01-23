apt_package ['python3-setuptools', 'python3-pygame', 'python3-pip', 'scanbd']
execute 'python3 -m pip install evdev spidev'

directory '/etc/scanbd/scripts'

template '/etc/scanbd/scripts/scan-script.sh' do
    source 'scan-script.sh'
end

user 'scan_user'

file "/etc/scanbd/scanbd.conf" do
    content lazy {
        IO.read("/etc/scanbd/scanbd.conf")
        .gsub(/[ \t]{2,}user\s+= ([^\s]+)/, "user = scan_user")
        .gsub("test.script", "scan-script.sh")
    }
end

require 'yaml'

data = YAML.load(IO.read("/etc/scanner/drive.yaml"), symbolize_names: true)

directory data[:mount][:folder]

replace_or_add "add scanner mount" do
    path "/etc/fstab"
    pattern "# scanner mount"
    line lazy {
        "%{path}\t%{folder}\t%{fs}\t%{options}\t0\t0 # scanner mount" % data[:mount]
    }
end
