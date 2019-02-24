using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
using System.Threading;
using System.IO;
namespace ConsoleApp1
{
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public class ScsiPassThroughDirect
    {
        public ushort Length;
        public byte ScsiStatus;
        public byte PathId;
        public byte TargetId;
        public byte Lun;
        public byte CdbLength;
        public byte SenseInfoLength;
        public byte DataIn;
        public byte pad1;
        public byte pad2;
        public byte pad3;
        public UInt32 DataTransferLength;
        public UInt32 TimeOutValue;
        public IntPtr DataBuffer; // UInt32 does not work on 64-bit
        public UInt32 SenseInfoOffset;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 16)]
        public byte[] Cdb;

        public ScsiPassThroughDirect(byte target, byte bus, byte lun, byte cdbLen, UInt32 dataTransferLength)
        {
            Length = (ushort)Marshal.SizeOf(typeof(ScsiPassThroughDirect));
            ScsiStatus = 0;
            PathId = bus;
            TargetId = target;
            Lun = lun;
            CdbLength = cdbLen;
            SenseInfoLength = 0;
            DataIn = 1;    // SCSI_IOCTL_DATA_IN
            DataTransferLength = dataTransferLength;
            TimeOutValue = 30;
            Cdb = new byte[16] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0 };
        }
    }

    public class DevIo
    {
        [DllImport("Kernel32.dll", SetLastError = false, CharSet = CharSet.Auto)]
        public static extern bool DeviceIoControl(
            IntPtr hDevice,
            uint IoControlCode,
            [MarshalAs(UnmanagedType.AsAny)]
        [In] object InBuffer,                           // should this be byte[]?  but how to pass sptwb
            uint nInBufferSize,
            [MarshalAs(UnmanagedType.AsAny)]
        [Out] object OutBuffer,
            uint nOutBufferSize,
            ref uint pBytesReturned,
            IntPtr Overlapped
        );
    }

    public class FileIo
    {
        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        public static extern IntPtr CreateFile(
             [MarshalAs(UnmanagedType.LPTStr)] string filename,
             [MarshalAs(UnmanagedType.U4)] FileAccess access,
             [MarshalAs(UnmanagedType.U4)] FileShare share,
             IntPtr securityAttributes, // optional SECURITY_ATTRIBUTES struct or IntPtr.Zero
             [MarshalAs(UnmanagedType.U4)] FileMode creationDisposition,
             [MarshalAs(UnmanagedType.U4)] FileAttributes flagsAndAttributes, IntPtr templateFile);
    }
    class Program
    {
        static void Main(string[] args)
        {

            // get file handle

            //string fileName = "\\\\.\\E:";
            string fileName = "\\\\.\\CdRom0";
            //string fileName = "\\\\.\\PhysicalDrive1";
            /*
            IntPtr x = FileIo.CreateFile(fileName,
                System.IO.FileAccess.ReadWrite,
                System.IO.FileShare.ReadWrite,
                IntPtr.Zero,
                System.IO.FileMode.Open,
                0,
                IntPtr.Zero);
             */
            IntPtr x = FileIo.CreateFile(fileName,
                System.IO.FileAccess.ReadWrite,
                System.IO.FileShare.Read,
                IntPtr.Zero,
                System.IO.FileMode.Open,
                0,
                IntPtr.Zero);

            if (x.ToInt32() == -1)
            {
                /* ask the framework to marshall the win32 error code to an exception */
            Marshal.ThrowExceptionForHR(Marshal.GetHRForLastWin32Error());
            }
            //
            uint BytesReturned = 0;

            ScsiPassThroughDirect sptd = new ScsiPassThroughDirect(0, 0, 0, 16, 0);
            sptd.Length = Convert.ToUInt16(Marshal.SizeOf(typeof(ScsiPassThroughDirect)));
            sptd.CdbLength = 16;
            sptd.DataIn = 0x01;  // SCSI_IOCTL_DATA_OUT;
            sptd.Cdb[0] = 0xd7; // sptwb.spt.Cdb[0] = SCSIOP_REWIND;
            sptd.Cdb[13] = 16;

            // DevIo call
            // 
            // need to confirm the IOCTL code for IOCTL_SCSI_PASS_THROUGH_DIRECT
            //
            bool ok = DevIo.DeviceIoControl(x, 0x4d014,
                sptd,
                (uint)Marshal.SizeOf(typeof(ScsiPassThroughDirect)),
                sptd,
                (uint)Marshal.SizeOf(typeof(ScsiPassThroughDirect)),
                ref BytesReturned,
                IntPtr.Zero);
            if (ok == false)
            {
                Marshal.ThrowExceptionForHR(Marshal.GetHRForLastWin32Error());
                //Console.WriteLine("DeviceIoControl failed with error: {0}", Marshal.GetLastWin32Error());
            }

        }
    }
}
