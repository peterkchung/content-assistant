"""
Orchestrator of the application.

"""

import models.base
import interface.chat





if __name__ == '__main__':

    interface.chat.chatUI.queue()
    interface.chat.chatUI.launch(show_api = False)