import openai
import os

from model.message_preparation import MessageBuilder
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    parser = GitHistoryDataSetParser("./")
    data = parser.load_data("history_scanner/test_save.dat")
    messages = MessageBuilder(data[-3:])
    for message in messages.get_train_messages():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(message)
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=f"{message}",
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#"]
        )
        print(response)


if __name__ == "__main__":
    main()