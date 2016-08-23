def get_templatename(file_template):
    '''
    Assess from hoc file the templatename being specified within

    Arguments
    ---------
    file_template : file, mode 'r'

    Returns
    -------
    templatename : str

    '''
    file_template = file("template.hoc", 'r')
    for line in file_template.readlines():
        if 'begintemplate' in line.split():
            templatename = line.split()[-1]
            continue

    return templatename
