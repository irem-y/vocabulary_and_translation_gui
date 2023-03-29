import os
import pytask

path_latex = os.path.join(os.path.dirname(__file__), "..", "..", "docs")


@pytask.mark.latex(script=os.path.join(path_latex,
                                       "project_documentation.tex"),
                   document=os.path.join(path_latex,
                                         "project_documentation.pdf"))
def task_compile_latex_document():
    pass
