import wpilib
import dashboard
import threading

class Robot(wpilib.IterativeRobot):

    def robotInit(self):
        frontLeft = wpilib.Victor(0)
        frontRight = wpilib.Victor(1)
        rearLeft = wpilib.Victor(2)
        rearRight = wpilib.Victor(3)
        self.robot_drive = wpilib.RobotDrive(frontLeftMotor=frontLeft,
                                             frontRightMotor=frontRight,
                                             rearLeftMotor=rearLeft,
                                             rearRightMotor=rearRight)
        self.joystick = wpilib.Joystick(0)

        self.gyro = wpilib.Gyro(0)
        #calibrate the gyro
        self.gyro_drift = 0.0
        wpilib.Timer.delay(2.0)
        last_angle = self.gyro.getAngle()
        wpilib.Timer.delay(10.0)
        self.gyro_drift = (self.gyro.getAngle() - last_angle) / 10.0

        self.timer = wpilib.Timer()

        self.dashboard = dashboard.Dashboard()
        def send_thread():
            while True:
                self.dashboard.send_udp(dashboard.encode_gyro(self.get_angle()))
                wpilib.Timer.delay(0.05)
        def recv_thread():
            while True:
                self.dashboard.get_msg()
        t_send = threading.Thread(target=send_thread)
        t_send.daemon = True
        t_send.start()
        t_recv = threading.Thread(target=recv_thread)
        t_recv.daemon = True
        #t_recv.start()

    def teleopInit(self):
        self.gyro.reset()
        self.timer.reset()

    def teleopPeriodic(self):
        x = self.gamepad.getX()
        y = self.gamepad.getY()
        rot = self.gamepad.getZ()
        self.drive(x, y, rot)
        wpilib.Timer.delay(0.005)

    def drive(self, x, y, rot):
        self.robot_drive.mecanumDrive_Cartesian(x, y, rot, 0)

    def get_angle(self):
        return self.gyro.getAngle() - self.gyro_drift * self.timer.get()

if __name__ == '__main__':
    wpilib.run(Robot)
