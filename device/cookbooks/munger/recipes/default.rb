apt_package ['python3-setuptools', 'python3-pygame', 'python3-pip', 'scanbd']
execute 'python3 -m pip install evdev spidev pyusb'

directory '/etc/scanbd/scripts'

user 'scan_user'

file "/etc/scanbd/scanbd.conf" do
    content lazy {
        IO.read("/etc/scanbd/scanbd.conf")
        .gsub(/[ \t]{2,}user\s+= ([^\s]+)/, "user = scan_user")
        .gsub("test.script", "scan-script.sh")
    }
end

directory '/etc/scanner'

if (File.exist?("/etc/scanner/drive.yaml"))
    require 'yaml'
    data = YAML.load(IO.read("/etc/scanner/drive.yaml"), symbolize_names: true)

    directory data[:mount][:mount_folder]

    mount data[:mount][:mount_folder] do
        device data[:mount][:path]
        fstype data[:mount][:fs]
        options data[:mount][:options]
        action [:mount, :enable]
    end

    template '/etc/scanbd/scripts/scan-script.sh' do
        source 'scan-script.sh'
        variables(out_dir: data[:mount][:mount_folder] + data[:mount][:scans_folder])
    end
end

replace_or_add 'spi config' do
    path '/boot/config.txt'
    pattern 'dtparam=spi=on'
    line 'dtparam=spi=on'
end

ruby_block '/boot/cmdline.txt' do
    block do
        unless File.exist?('/boot/cmdline.txt')
            File.open('/boot/cmdline.txt', 'w') do |f|
                f.write('rootwait')
            end
        end
        file = Chef::Util::FileEdit.new('/boot/cmdline.txt')
        file.search_file_replace(/rootwait.*/, "rootwait fbcon=map:10 consoleblank=")
        file.write_file
    end
end

file '/etc/modprobe.d/tft.conf' do
    content 'options fbtft_device name=pitft rotate=90'
end

cookbook_file '/etc/modules-load.d/tft.conf' do
    source 'tft.conf'
end

service 'ssh' do
    action [:enable, :start]
end

directory '/opt/munger'

cookbook_file '/opt/munger/watch.py' do
    source 'watch.py'
end

execute 'systemctl daemon-reload' do
    command 'systemctl daemon-reload'
    action :nothing
end

cookbook_file '/etc/systemd/system/watch.service' do
    source 'watch.service'
    notifies :run, 'execute[systemctl daemon-reload]', :immediately
    notifies :restart, 'service[watch]'
end

service 'watch' do
    provider Chef::Provider::Service::Systemd
    action [:enable, :start]
end