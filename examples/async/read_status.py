"""asyncio로 버전과 관절 좌표를 조회합니다. 자동 동작은 없습니다."""

import asyncio

from pf400 import AsyncPF400

# 실제 장비 주소와 필요한 값으로 수정한 뒤 이 파일을 실행하세요.
HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0


async def main():
    async with AsyncPF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        await robot.mode(0, channel="motion")
        await robot.mode(0, channel="status")
        await robot.select_robot(ROBOT_ID, channel="motion")
        await robot.select_robot(ROBOT_ID, channel="status")
        print("Version:", (await robot.version()).data)
        print("Joint positions:", (await robot.where_j()).as_floats())


if __name__ == "__main__":
    asyncio.run(main())
