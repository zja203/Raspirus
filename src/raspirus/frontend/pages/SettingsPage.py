import tkinter as tk
from raspirus.frontend.popups.SingleButtonDialog import SingleButtonDialog
# For colors and fonts
from raspirus.frontend.utility import \
    BACKGROUND_COLOR, SMALL_BUTTON_TEXT_FONT, \
    GREY_COLOR, NORMAL_TEXT_FONT, SUBTITLE_FONT, \
    TEXT_COLOR, SECONDARY_COLOR, WARNING_COLOR, FAILURE_COLOR
import time
import os


class SettingsPage(tk.Frame):
    home_btn: tk.Button
    title_label: tk.Label
    hash_label: tk.Label
    log_label: tk.Label
    ssh_label: tk.Label
    ftp_label: tk.Label
    hash_btn: tk.Button
    log_btn: tk.Button
    ssh_btn: tk.Button
    ftp_btn: tk.Button

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BACKGROUND_COLOR)

        # Button to return to the main page
        self.arrow_icon = tk.PhotoImage(file="frontend/images/icons/back_arrow.png")
        self.home_btn = tk.Button(self, text="HOME", font=SMALL_BUTTON_TEXT_FONT,
                                  image=self.arrow_icon, compound=tk.LEFT, padx=10,
                                  fg=BACKGROUND_COLOR, bg=GREY_COLOR)
        self.home_btn.config(command=lambda: controller.show_frame(controller.pages[0]))
        self.home_btn.place(x=20, y=30, width=110, height=30)

        # title of the page
        self.title_label = tk.Label(self, text="SETTINGS", font=SUBTITLE_FONT,
                                    fg=SECONDARY_COLOR, bg=BACKGROUND_COLOR)
        self.title_label.place(x=235, y=60, width=325, height=60)

        # All Labels
        self.hash_label = tk.Label(self, text="Update Hash signatures", font=NORMAL_TEXT_FONT,
                                   fg=TEXT_COLOR, bg=BACKGROUND_COLOR, anchor='w')
        self.hash_label.place(x=30, y=170, width=460, height=25)

        self.log_label = tk.Label(self, text="Open LOG window", font=NORMAL_TEXT_FONT,
                                  fg=TEXT_COLOR, bg=BACKGROUND_COLOR, anchor='w')
        self.log_label.place(x=30, y=240, width=460, height=25)

        self.ssh_label = tk.Label(self, text="Activate SSH", font=NORMAL_TEXT_FONT,
                                  fg=TEXT_COLOR, bg=BACKGROUND_COLOR, anchor='w')
        self.ssh_label.place(x=30, y=310, width=460, height=25)

        self.ftp_label = tk.Label(self, text="Activate FTP", font=NORMAL_TEXT_FONT,
                                  fg=TEXT_COLOR, bg=BACKGROUND_COLOR, anchor='w')
        self.ftp_label.place(x=30, y=380, width=460, height=25)

        # All icons
        prefix = "frontend/images/icons/"
        self.refresh_icon = tk.PhotoImage(file=prefix + "refresh_icon.png")
        self.cancel_icon = tk.PhotoImage(file=prefix + "cancel_sign.png")
        self.check_icon = tk.PhotoImage(file=prefix + "check_mark.png")
        self.logs_icon = tk.PhotoImage(file=prefix + "logs_book.png")

        # All Buttons
        self.hash_btn = tk.Button(self, text="Last updated 23.11.2022", font=NORMAL_TEXT_FONT,
                                  image=self.refresh_icon, compound=tk.LEFT, padx=10,
                                  fg=BACKGROUND_COLOR, bg=SECONDARY_COLOR)
        self.hash_btn.config(command=lambda: self.set_hash_status(controller))
        self.hash_btn.place(x=480, y=170, width=290, height=40)

        self.log_btn = tk.Button(self, text="", font=NORMAL_TEXT_FONT,
                                 image=self.logs_icon, compound=tk.LEFT, padx=10,
                                 fg=BACKGROUND_COLOR, bg=SECONDARY_COLOR)
        self.log_btn.config(command=lambda: controller.show_frame(controller.pages[6]))
        self.log_btn.place(x=480, y=240, width=290, height=40)
        self.set_logs_status(controller)

        self.ssh_btn = tk.Button(self, text="Work in Progress", font=NORMAL_TEXT_FONT,
                                 image=self.check_icon, compound=tk.LEFT, padx=10,
                                 fg=BACKGROUND_COLOR, bg=WARNING_COLOR)
        self.ssh_btn.config(command=lambda: self.set_ssh_status())
        self.ssh_btn.place(x=480, y=310, width=290, height=40)

        self.ftp_btn = tk.Button(self, text="Work in Progress", font=NORMAL_TEXT_FONT,
                                 image=self.cancel_icon, compound=tk.LEFT, padx=10,
                                 fg=BACKGROUND_COLOR, bg=WARNING_COLOR)
        self.ftp_btn.config(command=lambda: self.set_ftp_status())
        self.ftp_btn.place(x=480, y=380, width=290, height=40)

    def set_logs_status(self, controller):
        log_file_gen_text = "No Logs"
        if os.path.exists(controller.log_file_location):
            # Retrieves the modification time of the logs file and formats it accordingly
            gen_time = time.strptime(time.ctime(os.path.getmtime(controller.log_file_location)))
            log_file_gen_time = time.strftime("%d.%m.%Y %H:%M:%S", gen_time)
            log_file_gen_text = "UP: " + log_file_gen_time
        else:
            self.log_btn.config(bg=FAILURE_COLOR)

        self.log_btn.config(text=log_file_gen_text)

    def set_hash_status(self, controller):
        # TODO: Start an Signature update and display status
        self.hash_btn.config(text="Loading...")
        controller.start_hash_updates()

        hash_file_gen_text = "No Signatures!"
        if os.path.exists(controller.signature_path):
            # Retrieves the modification time of the logs file and formats it accordingly
            gen_time = time.strptime(time.ctime(os.path.getmtime(controller.signature_path)))
            hash_file_gen_time = time.strftime("%d.%m.%Y %H:%M:%S", gen_time)
            hash_file_gen_text = "UP: " + hash_file_gen_time
        else:
            self.hash_btn.config(bg=FAILURE_COLOR)

        self.hash_btn.config(text=hash_file_gen_text)

    def set_ssh_status(self):
        # TODO: Activate or deactivate SSH and display status
        # Set SUCCESS_COLOR (green) if active
        # Set FAILURE_COLOR (red) if shutdown
        dialog_message = "SSH allows you to connect to the Raspberry Pi remotely. " \
                         "Use this feature responsibly, as it might break the Raspberry Pi!"
        dialog = SingleButtonDialog(title="SSH maintenance", parent=self,
                                    message=dialog_message, mode="warning")
        dialog.tkraise()

    def set_ftp_status(self):
        # TODO: Activate or deactivate FTP and display status
        # Set SUCCESS_COLOR (green) if active
        # Set FAILURE_COLOR (red) if shutdown
        dialog_message = "FTP allows you to transfer files from and to the Raspberry Pi. " \
                         "This is usually used to retrieve logs or manually update signatures."
        dialog = SingleButtonDialog(title="FTP maintenance", parent=self,
                                    message=dialog_message, mode="warning")
        dialog.tkraise()