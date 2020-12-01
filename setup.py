import cx_Freeze

executables = [cx_Freeze.Executable(script = "main.py", 
                                    targetName = "ProjetoIA.exe")]
cx_Freeze.setup(
    name="Projeto I - IA",
    options={"build_exe": {"packages": ["pygame", "pathfinding"],
                           "include_files": ["./sprites/player.png", "./sprites/police.png", "bg_sound.ogg", "maze.png", "walls.txt"]
                           }},
    executables=executables
)

#PARA GERAR EXECUTÁVEL
# python -m pip install cx_Freeze --upgrade
# python setup.py build
# OBS:
# Por enquanto não consegui que o Freeze gerasse a pasta sprites, 
# então criar manualmente a pasta e colocar os arquivos "player.png" e "police.png" dentro.