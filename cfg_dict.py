import logging

COMMENT_TOKEN = '#'

class CfgDict():
    
    def __init__(self, file_path):
        super().__init__()
        self.path = file_path
        self.lines = []
        self.settings = {}

        self.__import()
      
    def __import(self):
         
        try:
            with open(self.path) as f:
                for line in f:
                    line = line.strip()
                    self.lines.append(line)
        except Exception as err:
            logging.error(err, exc_info=True)

        self.__extract_settings()

    def __extract_settings(self):

        for index, line in enumerate(self.lines):
            if not line: continue
            
            if line.startswith(COMMENT_TOKEN): continue
            tokens = line.split('=', 1)

            for i, _ in enumerate(tokens): 
                tokens[i] = tokens[i].strip()
                if tokens[i].isdigit():
                    tokens[i] = int(tokens[i])

            if len(tokens) != 2:
                logging.warning(
                    'skipping improper line in "%s": \'%s\''
                    % (self.path, line))
                continue

            setting, value = tokens
            if setting in self.settings:
                logging.warning(
                    'ignoring duplicate setting in "%s": \'%s\''
                    % (self.path, line))
                continue
            self.settings[setting] = (value, index)

    def __update_list(self):
        for setting, value in self.settings.items():
            self.lines[value[1]] = '%s = %s' % (setting, value[0])

    def export(self):
        self.__update_list()
        with open(self.path, 'w') as f:
            for line in self.lines:
                f.write('%s\n' % line)

    def __getitem__(self, key):
        return self.settings[key][0]

    def __setitem__(self, key, value):
        if key not in self.settings:
            logging.warning(
                'attempted to change non-existant setting in %s: \'%s\''
                % (self.path, key))
            return None
        pair = self.settings[key]
        self.settings[key] = (value, pair[1])
        return self.__getitem__(key)
