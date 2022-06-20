from pathlib import Path
import uuid

from eval.CompilerEvaluator import CompilerEvaluator
from generation.Model import Model
from generation.GeneratedTestSaver import GeneratedTestSaver
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
from eval.BLEUEvaluator import BLEUEvaluator

model = Model()


def main():
    bleu = BLEUEvaluator()
    compiler = CompilerEvaluator(Path("../dataset_repos/flask"), "env\\Scripts\\activate")
    parser = GitHistoryDataSetParser("dataset_repos/flask")
    # parser.parse_data()
    # parser.save_parsed_data("dataset_repos/data/flask_test.dat")
    # data = parser.get_parsed_data()
    data = parser.load_data("dataset_repos/data/flask_test.dat")
    print(f"Generating tests for {len(data)} commits")

    for commit in data:
        saver = GeneratedTestSaver(str(Path("dataset_repos/flask").absolute()), commit.commit_id)
        saver.goto_commit()
        for prompt in commit.construct_prompt():
            try:
                test = model.generate_test(str(prompt))
                file_path = saver.save_test_file(prompt, test, f'test_{uuid.uuid4()}')
                bleu.evaluate(test, commit.test_files, commit.commit_id)
                compiler.evaluate(file_path)
            except Exception as e:
                print(e)
        saver.commit_files()
        saver.clean_state()
    bleu.export()
    compiler.export()


if __name__ == "__main__":
    main()
