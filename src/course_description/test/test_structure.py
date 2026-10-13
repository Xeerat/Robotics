import os
import subprocess
import xml.etree.ElementTree as ET

import pytest

PKG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XACRO = os.path.join(PKG_DIR, 'urdf', 'vehicle.urdf.xacro')


def _expand():
    out = subprocess.run(
        ['xacro', XACRO],
        capture_output=True, text=True, check=True
    )
    return out.stdout


def _parse():
    xml_str = _expand()
    return ET.fromstring(xml_str)


def test_xacro_expands():
    xml_str = _expand()
    assert '<robot' in xml_str
    assert 'course_ackermann' in xml_str


def test_check_urdf_passes():
    xml_str = _expand()
    tmp = '/tmp/vehicle.urdf'
    with open(tmp, 'w') as f:
        f.write(xml_str)
    res = subprocess.run(['check_urdf', tmp], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr


def test_lidar_parent_is_base_link():
    """Ключевой тест для стадии 'сломать/доказать'."""
    root = _parse()
    for joint in root.findall('joint'):
        if joint.get('name') == 'lidar_joint':
            parent = joint.find('parent').get('link')
            assert parent == 'base_link', (
                f'lidar_joint parent must be base_link, got {parent}'
            )
            return
    pytest.fail('lidar_joint not found')


def test_all_sensors_present():
    root = _parse()
    links = {link.get('name') for link in root.findall('link')}
    for needed in ('base_link', 'lidar_link', 'camera_link', 'imu_link'):
        assert needed in links, f'missing link {needed}'


def test_fixed_joints_have_origin():
    root = _parse()
    for joint in root.findall('joint'):
        if joint.get('type') == 'fixed':
            origin = joint.find('origin')
            assert origin is not None, (
                f'fixed joint {joint.get("name")} has no origin'
            )
