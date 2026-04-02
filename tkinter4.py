import ast
import operator
import re
from tkinter import StringVar, Text, Tk, ttk, END

from Storehistory import Storehistory


class SafeEvaluator:
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression):
        parsed = ast.parse(expression, mode="eval")
        return cls._visit(parsed.body)

    @classmethod
    def _visit(cls, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in cls.OPERATORS:
            return cls.OPERATORS[type(node.op)](cls._visit(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in cls.OPERATORS:
            left = cls._visit(node.left)
            right = cls._visit(node.right)
            return cls.OPERATORS[type(node.op)](left, right)
        raise ValueError("Only math expressions are supported.")


class ChatBotCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Studio")
        self.root.geometry("1080x760")
        self.root.minsize(980, 700)

        self.history = Storehistory("results.txt")
        self.expression_var = StringVar()
        self.mode_var = StringVar(value="Add")
        self.solver_result_var = StringVar(value="Choose a mode and enter values.")
        self.basic_result_var = StringVar(value="0")

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4efe6")
        style.configure("Card.TFrame", background="#fffaf4")
        style.configure("Header.TLabel", background="#f4efe6", foreground="#203239", font=("Georgia", 24, "bold"))
        style.configure("Sub.TLabel", background="#f4efe6", foreground="#385170", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#fffaf4", foreground="#203239", font=("Georgia", 14, "bold"))
        style.configure("Result.TLabel", background="#fffaf4", foreground="#0f5132", font=("Consolas", 16, "bold"))
        style.configure("Hint.TLabel", background="#fffaf4", foreground="#5c6770", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        self.root.configure(bg="#f4efe6")

    def _build_ui(self):
        outer = ttk.Frame(self.root, style="App.TFrame", padding=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Calculator Studio", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Standard calculator, guided solver, and a math helper chatbot in one app.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)

        calculator_tab = ttk.Frame(notebook, style="App.TFrame", padding=12)
        solver_tab = ttk.Frame(notebook, style="App.TFrame", padding=12)
        chat_tab = ttk.Frame(notebook, style="App.TFrame", padding=12)

        notebook.add(calculator_tab, text="Calculator")
        notebook.add(solver_tab, text="Solver Modes")
        notebook.add(chat_tab, text="Math Chat")

        self._build_calculator_tab(calculator_tab)
        self._build_solver_tab(solver_tab)
        self._build_chat_tab(chat_tab)

    def _build_calculator_tab(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Expression Calculator", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            card,
            text="Use +, -, *, /, //, %, ** and parentheses. Example: (12 + 8) / 5",
            style="Hint.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        entry = ttk.Entry(card, textvariable=self.expression_var, font=("Consolas", 18), width=28)
        entry.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        entry.focus()

        ttk.Label(card, text="Result", style="CardTitle.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(card, textvariable=self.basic_result_var, style="Result.TLabel").grid(row=4, column=0, sticky="w", pady=(4, 16))

        pad = ttk.Frame(card, style="Card.TFrame")
        pad.grid(row=5, column=0, sticky="nsew")

        buttons = [
            ["7", "8", "9", "/", "Clear"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", ".", "%", "+", "**"],
            ["//", "Back", "Ans", "=", ""],
        ]

        for r_index, row in enumerate(buttons):
            for c_index, label in enumerate(row):
                if not label:
                    continue
                command = lambda value=label: self._handle_calculator_button(value)
                ttk.Button(pad, text=label, command=command, style="Accent.TButton").grid(
                    row=r_index, column=c_index, padx=6, pady=6, sticky="nsew"
                )

        for index in range(5):
            pad.columnconfigure(index, weight=1)
        for index in range(5):
            pad.rowconfigure(index, weight=1)

        card.columnconfigure(0, weight=1)
        card.rowconfigure(5, weight=1)

    def _build_solver_tab(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Guided Problem Solver", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(
            card,
            text="Choose a method for solving: direct operations, averages, percentages, powers, and more.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 14))

        ttk.Label(card, text="Mode", style="Hint.TLabel").grid(row=2, column=0, sticky="w")
        mode_box = ttk.Combobox(
            card,
            textvariable=self.mode_var,
            state="readonly",
            values=["Add", "Subtract", "Multiply", "Divide", "Average", "Power", "Percent Of", "Percent Change"],
            width=20,
        )
        mode_box.grid(row=3, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))
        mode_box.bind("<<ComboboxSelected>>", lambda _event: self._update_solver_hint())

        self.solver_hint = ttk.Label(card, text="", style="Hint.TLabel")
        self.solver_hint.grid(row=3, column=1, columnspan=2, sticky="w")

        self.solver_entries = []
        for index in range(3):
            ttk.Label(card, text=f"Value {index + 1}", style="Hint.TLabel").grid(row=4 + index * 2, column=0, sticky="w")
            entry = ttk.Entry(card, font=("Consolas", 14), width=18)
            entry.grid(row=5 + index * 2, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))
            self.solver_entries.append(entry)

        button_row = ttk.Frame(card, style="Card.TFrame")
        button_row.grid(row=10, column=0, columnspan=3, sticky="w", pady=(6, 16))
        ttk.Button(button_row, text="Solve", command=self.solve_guided_problem, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(button_row, text="Clear Fields", command=self.clear_solver_fields).pack(side="left")

        ttk.Label(card, text="Answer", style="CardTitle.TLabel").grid(row=11, column=0, sticky="w")
        ttk.Label(card, textvariable=self.solver_result_var, style="Result.TLabel", wraplength=760, justify="left").grid(
            row=12, column=0, columnspan=3, sticky="w", pady=(4, 10)
        )

        self.solver_steps = Text(card, height=11, width=70, font=("Consolas", 11), bg="#fff7eb", fg="#203239", bd=0, padx=10, pady=10)
        self.solver_steps.grid(row=13, column=0, columnspan=3, sticky="nsew")
        self.solver_steps.insert("1.0", "Step-by-step work will appear here.")
        self.solver_steps.config(state="disabled")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)
        card.columnconfigure(2, weight=1)
        card.rowconfigure(13, weight=1)
        self._update_solver_hint()

    def _build_chat_tab(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Math Helper Chat", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            card,
            text="Ask for a calculation or for help. Try: 'what is 45 * 12', 'average 4 7 10', or 'how do I solve percentages?'",
            style="Hint.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        self.chat_history = Text(card, height=20, font=("Segoe UI", 11), bg="#fff7eb", fg="#203239", bd=0, padx=12, pady=12, wrap="word")
        self.chat_history.grid(row=2, column=0, sticky="nsew")
        self.chat_history.insert("1.0", "Bot: I can solve expressions, averages, powers, percent problems, and explain which mode to use.\n")
        self.chat_history.config(state="disabled")

        input_row = ttk.Frame(card, style="Card.TFrame")
        input_row.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        self.chat_entry = ttk.Entry(input_row, font=("Segoe UI", 12))
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.chat_entry.bind("<Return>", lambda _event: self.send_chat_message())
        ttk.Button(input_row, text="Send", command=self.send_chat_message, style="Accent.TButton").pack(side="left")

        examples = ttk.Frame(card, style="Card.TFrame")
        examples.grid(row=4, column=0, sticky="w", pady=(12, 0))
        for sample in [
            "what is (8+2)*5",
            "average 4 7 10",
            "25 percent of 80",
            "how do i divide decimals",
        ]:
            ttk.Button(examples, text=sample, command=lambda text=sample: self._prefill_chat(text)).pack(side="left", padx=(0, 6))

        card.columnconfigure(0, weight=1)
        card.rowconfigure(2, weight=1)

    def _handle_calculator_button(self, value):
        if value == "Clear":
            self.expression_var.set("")
            self.basic_result_var.set("0")
            return
        if value == "Back":
            self.expression_var.set(self.expression_var.get()[:-1])
            return
        if value == "Ans":
            self.expression_var.set(self.expression_var.get() + self.basic_result_var.get())
            return
        if value == "=":
            self.solve_expression()
            return
        self.expression_var.set(self.expression_var.get() + value)

    def solve_expression(self):
        expression = self.expression_var.get().strip()
        if not expression:
            self.basic_result_var.set("Enter an expression first.")
            return
        try:
            result = SafeEvaluator.evaluate(expression)
            self.basic_result_var.set(self._format_number(result))
            self._store_result(f"Expression: {expression} = {self._format_number(result)}")
        except Exception as error:
            self.basic_result_var.set(f"Error: {error}")

    def solve_guided_problem(self):
        mode = self.mode_var.get()
        raw_values = [entry.get().strip() for entry in self.solver_entries]
        try:
            values = [float(value) for value in raw_values if value]
        except ValueError:
            self.solver_result_var.set("Please enter valid numbers.")
            self._write_solver_steps("I could not solve that because one of the values is not a number.")
            return

        try:
            answer, steps = self._solve_mode(mode, values)
            answer_text = f"{mode}: {self._format_number(answer)}"
            self.solver_result_var.set(answer_text)
            self._write_solver_steps(steps)
            self._store_result(f"{mode}: inputs={values} result={self._format_number(answer)}")
        except Exception as error:
            self.solver_result_var.set(str(error))
            self._write_solver_steps("Adjust the inputs or switch modes, then try again.")

    def _solve_mode(self, mode, values):
        if mode in {"Add", "Subtract", "Multiply", "Divide"} and len(values) < 2:
            raise ValueError("This mode needs at least two values.")
        if mode == "Average" and len(values) < 1:
            raise ValueError("Average needs at least one value.")
        if mode == "Power" and len(values) != 2:
            raise ValueError("Power needs exactly two values: base and exponent.")
        if mode == "Percent Of" and len(values) != 2:
            raise ValueError("Percent Of needs exactly two values: percent and total.")
        if mode == "Percent Change" and len(values) != 2:
            raise ValueError("Percent Change needs exactly two values: original and new value.")

        if mode == "Add":
            answer = sum(values)
            steps = f"Add the numbers together:\n" + "\n".join(f"  running total -> {self._format_number(sum(values[:index + 1]))}" for index in range(len(values)))
            return answer, steps
        if mode == "Subtract":
            answer = values[0]
            lines = [f"Start with {self._format_number(answer)}"]
            for value in values[1:]:
                answer -= value
                lines.append(f"Subtract {self._format_number(value)} -> {self._format_number(answer)}")
            return answer, "\n".join(lines)
        if mode == "Multiply":
            answer = 1
            lines = []
            for value in values:
                answer *= value
                lines.append(f"Multiply by {self._format_number(value)} -> {self._format_number(answer)}")
            return answer, "\n".join(lines)
        if mode == "Divide":
            answer = values[0]
            lines = [f"Start with {self._format_number(answer)}"]
            for value in values[1:]:
                if value == 0:
                    raise ValueError("Division by zero is not allowed.")
                answer /= value
                lines.append(f"Divide by {self._format_number(value)} -> {self._format_number(answer)}")
            return answer, "\n".join(lines)
        if mode == "Average":
            total = sum(values)
            answer = total / len(values)
            steps = (
                f"1. Add the values: {self._format_number(total)}\n"
                f"2. Count how many values there are: {len(values)}\n"
                f"3. Divide total by count: {self._format_number(total)} / {len(values)} = {self._format_number(answer)}"
            )
            return answer, steps
        if mode == "Power":
            base, exponent = values
            answer = base ** exponent
            steps = f"Raise the base to the exponent:\n{self._format_number(base)} ^ {self._format_number(exponent)} = {self._format_number(answer)}"
            return answer, steps
        if mode == "Percent Of":
            percent, total = values
            answer = (percent / 100) * total
            steps = (
                f"1. Convert percent to decimal: {self._format_number(percent)} / 100 = {self._format_number(percent / 100)}\n"
                f"2. Multiply by total: {self._format_number(percent / 100)} * {self._format_number(total)} = {self._format_number(answer)}"
            )
            return answer, steps
        if mode == "Percent Change":
            original, new_value = values
            if original == 0:
                raise ValueError("Original value cannot be zero for percent change.")
            difference = new_value - original
            answer = (difference / original) * 100
            steps = (
                f"1. Find the difference: {self._format_number(new_value)} - {self._format_number(original)} = {self._format_number(difference)}\n"
                f"2. Divide by the original value: {self._format_number(difference)} / {self._format_number(original)} = {self._format_number(difference / original)}\n"
                f"3. Convert to percent: {self._format_number(answer)}%"
            )
            return answer, steps
        raise ValueError("Unsupported mode selected.")

    def clear_solver_fields(self):
        for entry in self.solver_entries:
            entry.delete(0, END)
        self.solver_result_var.set("Choose a mode and enter values.")
        self._write_solver_steps("Step-by-step work will appear here.")

    def _update_solver_hint(self):
        hints = {
            "Add": "Enter two or three values to combine.",
            "Subtract": "Enter a starting value, then the values to subtract.",
            "Multiply": "Enter two or three values to multiply.",
            "Divide": "Enter a starting value, then the divisors.",
            "Average": "Enter as many values as you want to average.",
            "Power": "Value 1 = base, Value 2 = exponent.",
            "Percent Of": "Value 1 = percent, Value 2 = total.",
            "Percent Change": "Value 1 = original, Value 2 = new value.",
        }
        self.solver_hint.config(text=hints.get(self.mode_var.get(), ""))

    def send_chat_message(self):
        message = self.chat_entry.get().strip()
        if not message:
            return
        self.chat_entry.delete(0, END)
        self._append_chat("You", message)
        reply = self._chatbot_reply(message)
        self._append_chat("Bot", reply)

    def _chatbot_reply(self, message):
        lowered = message.lower().strip()

        if any(phrase in lowered for phrase in ["how do i", "help", "explain", "what mode"]):
            return self._chat_help(lowered)

        try:
            numbers = [float(match) for match in re.findall(r"-?\d+(?:\.\d+)?", lowered)]

            if "average" in lowered and numbers:
                answer, _ = self._solve_mode("Average", numbers)
                return f"The average is {self._format_number(answer)}. You can also use Solver Modes > Average for step-by-step work."

            if "percent change" in lowered and len(numbers) >= 2:
                answer, _ = self._solve_mode("Percent Change", numbers[:2])
                return f"The percent change is {self._format_number(answer)}%."

            if "percent of" in lowered and len(numbers) >= 2:
                answer, _ = self._solve_mode("Percent Of", numbers[:2])
                return f"{self._format_number(numbers[0])}% of {self._format_number(numbers[1])} is {self._format_number(answer)}."

            if "power" in lowered and len(numbers) >= 2:
                answer, _ = self._solve_mode("Power", numbers[:2])
                return f"{self._format_number(numbers[0])} to the power of {self._format_number(numbers[1])} is {self._format_number(answer)}."

            cleaned = lowered.replace("what is", "").replace("calculate", "").replace("=", "").strip()
            if re.fullmatch(r"[-+*/%().\s\d]+", cleaned) or "//" in cleaned or "**" in cleaned:
                answer = SafeEvaluator.evaluate(cleaned)
                self._store_result(f"Chat expression: {cleaned} = {self._format_number(answer)}")
                return f"The answer is {self._format_number(answer)}."
        except Exception:
            pass

        return (
            "I can help with expressions, averages, powers, percentages, and percent change. "
            "Try a message like 'what is 9*(4+1)' or '25 percent of 80'."
        )

    def _chat_help(self, lowered):
        if "percent" in lowered:
            return "For percent-of problems, use the formula percent / 100 * total. Example: 25% of 80 = 0.25 * 80 = 20."
        if "divide" in lowered:
            return "For division, put the starting number first, then divide by each value after it. In Solver Modes you can see each step."
        if "average" in lowered or "mean" in lowered:
            return "To find an average, add all values together and divide by how many numbers there are."
        if "mode" in lowered:
            return "Use Calculator for typed expressions, Solver Modes for guided steps, and Math Chat for quick questions in plain language."
        return "You can ask me to explain percentages, averages, powers, or which tab to use for a problem."

    def _append_chat(self, speaker, message):
        self.chat_history.config(state="normal")
        self.chat_history.insert(END, f"{speaker}: {message}\n")
        self.chat_history.see(END)
        self.chat_history.config(state="disabled")

    def _prefill_chat(self, text):
        self.chat_entry.delete(0, END)
        self.chat_entry.insert(0, text)
        self.send_chat_message()

    def _write_solver_steps(self, text):
        self.solver_steps.config(state="normal")
        self.solver_steps.delete("1.0", END)
        self.solver_steps.insert("1.0", text)
        self.solver_steps.config(state="disabled")

    def _store_result(self, text):
        self.history.save_result(text)

    @staticmethod
    def _format_number(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.6f}".rstrip("0").rstrip(".")


def main():
    root = Tk()
    ChatBotCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
