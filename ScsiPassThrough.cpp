// ConsoleApplication2.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#define _NTSCSI_USER_MODE_
#include <windows.h>
#include <scsi.h>
#include <ntddscsi.h>
#include "pch.h"
#include <iostream>
#define MAXULONG                            0xFFFFFFFF  // winnt
#define MAXUSHORT   0xffff      // winnt
BOOL scsi_read(HANDLE fh, PVOID buf, DWORD cb, ULONGLONG LogicalBlock, ULONG TransferBlocks)
{
	SCSI_PASS_THROUGH_DIRECT s = {
		//sizeof(SCSI_PASS_THROUGH_DIRECT), 0, 0, 0, 0, 0, 0, SCSI_IOCTL_DATA_IN, cb, 30, buf
		sizeof(SCSI_PASS_THROUGH_DIRECT), 0, 0, 0, 0, 0, 0, SCSI_IOCTL_DATA_IN, cb, 30, buf
	};

	union {
		PUCHAR Cdb;
		CDB::_CDB10* Cdb10;
		CDB::_CDB16* Cdb16;
	};

	Cdb = s.Cdb;
/*
	if (MAXULONG < LogicalBlock || MAXUSHORT < TransferBlocks)
	{*/
		s.CdbLength = sizeof(CDB::_CDB16);
		Cdb16->OperationCode = 0xd7;
		*(ULONGLONG*)Cdb16->LogicalBlock = _byteswap_uint64(LogicalBlock);
		*(ULONG*)Cdb16->TransferLength = _byteswap_ulong(TransferBlocks);/*
	}
	else
	{
		s.CdbLength = sizeof(CDB::_CDB10);
		Cdb10->OperationCode = 0xd7;
		*(ULONG*)&Cdb10->LogicalBlockByte0 = _byteswap_ulong((ULONG)LogicalBlock);
		*(USHORT*)&Cdb10->TransferBlocksMsb = _byteswap_ushort((USHORT)TransferBlocks);
	} */

	DWORD ioctl_bytes;

	return DeviceIoControl(fh, IOCTL_SCSI_PASS_THROUGH_DIRECT, &s, sizeof(s), &s, sizeof(s), &ioctl_bytes, NULL);
}

BOOL test_scsi_read(PCWSTR fname)
{
	BOOL fOk = FALSE;

	HANDLE fh = CreateFileW(fname, GENERIC_READ | GENERIC_WRITE,
		FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

	if (fh != INVALID_HANDLE_VALUE)
	{



				//fOk = scsi_read(fh, buf, 0, 0, 16);
				fOk = scsi_read(fh, 0, 0, 0, 16);


		CloseHandle(fh);
	}

	return fOk;
}

int main()
{
	test_scsi_read(L"\\\\?\\e:");
    std::cout << "Hello World!\n"; 
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
