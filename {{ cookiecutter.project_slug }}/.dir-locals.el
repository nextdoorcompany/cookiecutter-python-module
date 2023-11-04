;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (progn
                   (setq-local compile-command "doit")))))
 (python-mode . ((eval . (progn
                           (setq-local gud-pdb-command-name "{{ cookiecutter.path_to_venv }}/bin/python -m pdb")
                           (setq-local python-shell-virtualenv-root "{{ cookiecutter.path_to_venv }}"))))))
