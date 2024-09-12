# *_*coding:utf-8 *_*
import socket
from typing import Optional


class IPAddressManager:
    _instance: Optional['IPAddressManager'] = None
    _local_ip: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_local_ip(cls) -> Optional[str]:
        """获取本机的IP地址"""
        if cls._local_ip is None:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    cls._local_ip = s.getsockname()[0]
            except Exception as e:
                print(f"获取IP地址时发生错误: {e}")
        return cls._local_ip

    @classmethod
    def local_ip(cls) -> Optional[str]:
        """本机IP地址的类方法访问器"""
        return cls.get_local_ip()

    def __str__(self) -> str:
        return f"本机IP地址: {self.local_ip() or '未知'}"

    def __repr__(self) -> str:
        return f"IPAddressManager(local_ip={self.local_ip()!r})"


# 使用示例
if __name__ == "__main__":
    # 直接使用类方法访问，无需实例化
    print(f"本机IP地址: {IPAddressManager.local_ip()}")

    # 如果需要实例，仍然可以创建
    ip_manager = IPAddressManager()
    print(ip_manager)

    # 验证单例模式
    another_manager = IPAddressManager()
    print(f"是否为同一实例: {ip_manager is another_manager}")
