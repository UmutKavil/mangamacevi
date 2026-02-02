import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

export async function DELETE(
  request: NextRequest,
  { params }: { params: { fileId: string } }
) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/cleanup/${params.fileId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error = await response.json();
      return NextResponse.json(error, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Cleanup failed:', error);
    return NextResponse.json(
      { detail: 'Dosya temizleme başarısız oldu' },
      { status: 500 }
    );
  }
}
