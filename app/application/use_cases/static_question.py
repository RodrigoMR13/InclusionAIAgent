
class StaticQuestionUseCase:
    @staticmethod
    def execute(num_question: str) -> str:
        if num_question == "1":
            return "O que é superdotação?"
        elif num_question == "2":
            return "Como identificar altas habilidades?"
        elif num_question == "3":
            return "Quais direitos legais garantem inclusão escolar?"
        elif num_question == "4":
            return "Quais estratégias ajudam professores em sala de aula?"
        else:
            return "Opção inválida. Por favor, escolha uma opção entre 1 e 4."