%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-gazebo-video-monitor-plugins
Version:        0.8.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS gazebo_video_monitor_plugins package

License:        GPLv3
Source0:        %{name}-%{version}.tar.gz

Requires:       opencv-devel
Requires:       ros-humble-gazebo-dev
Requires:       ros-humble-gazebo-ros
Requires:       ros-humble-gazebo-video-monitor-interfaces
Requires:       ros-humble-rclcpp
Requires:       ros-humble-std-srvs
Requires:       ros-humble-ros-workspace
BuildRequires:  opencv-devel
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-gazebo-dev
BuildRequires:  ros-humble-gazebo-ros
BuildRequires:  ros-humble-gazebo-video-monitor-interfaces
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-std-srvs
BuildRequires:  ros-humble-yaml-cpp-vendor
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
gazebo_video_monitor_plugins is a package that lets the user record videos of a
Gazebo simulation. It provides a multicamera sensor that can be used for
creating different types of videos with multiple views from inside the gazebo
world. There is a number of plugins already available in the package, but more
can be developed by the user, with minimal effort, to fit arbitrary use cases.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Mon Nov 13 2023 Nick Lamprianidis <info@nlamprian.me> - 0.8.1-1
- Autogenerated by Bloom

* Sun Nov 12 2023 Nick Lamprianidis <info@nlamprian.me> - 0.8.0-1
- Autogenerated by Bloom

