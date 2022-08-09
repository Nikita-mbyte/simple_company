from dataclasses import dataclass, field
import random
from typing import ClassVar
import copy


@dataclass
class Project:
    _id: ClassVar[int] = -1

    def __init__(self, day):
        self.day_accepted: int = day
        self.type_project = random.choice(['mob', 'web'])
        self.level_project: int = random.randint(1, 3)
        self.id = Project._id
        Project._id += 1
        self.is_ready: bool = False
        self.is_ready_test: bool = False
        self.to_test: bool = False
        self.accepted_to_test: bool = False
        self.is_accepted: bool = False
        self.programmers: list = []

    def __str__(self):
        return f"id = {self.id}, level = {self.level_project}, type = " \
               f" {self.type_project},| test - {self.is_ready_test}" \
               f" | проект готов - {self.is_ready}"

@dataclass
class Programmer:
    type: str
    day_not_work: int = 0
    count_projects: int = 0
    is_busy: bool = False
    days_work: int = 0
    day_accepted: int = 0
    dismiss: bool = False
    project: Project = Project(0)

    id: int = field(init=False)
    _id: ClassVar[int] = 1

    def accept_project(self, project: Project):
        # Accetpting projects by difficulty levels
        self.project = project
        self.project.is_accepted = True
        self.is_busy = True
        self.day_accepted = day
        self.project.day_accepted = day
        self.days_work = self.project.level_project
        if project.to_test == True:
            self.project.programmers.clear()
            self.days_work = 1
            self.project.accepted_to_test = True
        self.project.programmers.append(self)
        if len(self.project.programmers) == 2:
            self.project.programmers[0].days_work = 1
            self.project.programmers[1].days_work = 1
        if len(self.project.programmers) == 3:
            self.project.programmers[0].days_work = 1
            self.project.programmers[1].days_work = 1
            self.project.programmers[2].days_work = 1

    def test_project(self):
        #This function checks is the project tested by employees
        if self.days_work == 0:
            self.is_busy = False
            self.count_projects += 1
            self.day_not_work = 0
            self.project.is_ready_test = True
            self.project.programmers.clear()
            print(f"проект {self.project.id} протестирован --- {self.id}")
        else:
            self.project.is_ready_test = False
            self.day_not_work = 0
            self.days_work -= 1

    def solve_project(self):
        #This function checks is the project solved by web/mob employees
        if self.days_work == 0:
            self.project.is_ready = True
            self.is_busy = False
            self.day_not_work = 0
            self.project.to_test = True
            for i in self.project.programmers:
                i.count_projects += 1
            print(f"Проект {self.project} готов {self.project.is_ready},  день -"
                  f" {day}, программсит "
                  f"{self.project.programmers} is busy {self.is_busy} !!!")
        else:
            self.project.is_ready = False
            self.day_not_work = 0
            self.days_work -= 1

    def __post_init__(self):
        self.id = Programmer._id
        Programmer._id += 1

    def __repr__(self):
        return f"{self.type} проограммист id - {self.id}, уволен - {self.dismiss}, " \
               f"проекты" \
               f" {self.project}," \
               f"занят {self.is_busy}, день принятия {self.day_accepted}, проекты " \
               f"дней без работы {self.day_not_work}, количесвто проектов {self.count_projects}"


@dataclass
class Department:
    projects: list = field(default_factory=list)
    programmers: list = field(default_factory=list)
    free_programmers: int = 0
    real_project: int = 0
    employes: int = 0
    dismissed: int = 0

    def get_free_programmers(self):
        # Return count free programeers on departments
        self.free_programmers = 0
        for p in self.programmers:
            if p.is_busy == False:
                self.free_programmers += 1
        return self.free_programmers

    def get_projects(self, project: Project):
        # This function get project if department have free programmers
        if self.free_programmers > 0:
            temp = copy.deepcopy(project)
            project.is_accepted = True
            temp.is_accepted = False
            self.projects.append(temp)
            self.free_programmers -= 1
            print(f"в {self} получен проект {project}")
            return True
        else:
            return False

    def add_programmers(self, type:str):
        self.programmers.append(Programmer(type))
        Department.employes += 1
        print(f'в{self} нанят программист id - {self.programmers[-1].id}')

    def solve_projects(self):
        # This function distributes one accepted project to each free programmer and
        # programmers start working
        for D in self.projects:
            if D.is_ready == False and D.is_accepted == False:
                self.send_projects(D)

        # After the projects are distributed, the programmers start working
        for p in self.programmers:
            if (p.dismiss == False and
                    p.project.is_accepted == True and
                    p.project.is_ready == False):
                p.solve_project()

    def send_projects(self, project: Project):
        # This function distributes accepted projects to departments  by free
        # programmers
        for p in self.programmers:
            if (p.is_busy == False and p.dismiss == False):
                p.accept_project(project)
                break

    def _chek_dismiss(self):
        # This function counts days when programmers did not work
        for p in self.programmers:
            if (p.is_busy == False and p.dismiss == False):
                p.day_not_work += 1
                # print(f"программист {p.id} без работы {p.day_not_work}")

    def _dismiss(self):
        # This function search dismissed and counts dismissed employees
        self._chek_dismiss()
        dismiss: Programmer
        temp = [p for p in self.programmers if p.day_not_work > 3 and p.dismiss == False]
        if temp:
            dismiss = temp[0]
            for i in range(1, len(temp)):
                if dismiss.count_projects > temp[i].count_projects:
                    dismiss = temp[i]
            print(f"программист {dismiss.id} уволен")
            Department.dismissed += 1
            dismiss.dismiss = True
            self.programmers.remove(dismiss)


@dataclass
class Web_Department(Department):

    def __str__(self):
        return "Web_Departament"


@dataclass
class Mob_Department(Department):

    def solve_projects(self):
        #This function distributes one accepted project to each free programmer and
        # mob_programmers start working
        for D in self.projects:
            if D.is_ready == False and D.is_accepted == False:
                self.send_projects(D)

                # If there are free programmers, we distribute depending on the complexity
                for D in self.projects:
                    temp = self.get_free_programmers()
                    if temp > 1:
                        if (D.is_ready == False and day == D.day_accepted):
                            if D.level_project == 2:
                                self.send_projects(D)
                                D.days_work = 1
                                temp -= 1
                            if D.level_project == 3:
                                self.send_projects(D)
                                self.send_projects(D)
                                temp -= 2
                    elif self.get_free_programmers() == 1:
                        if (D.is_ready == False and day == D.day_accepted):
                            if D.level_project == 2:
                                self.send_projects(D)
                                temp -= 1

        for p in self.programmers:
            if (p.dismiss == False and
                    p.project.is_accepted == True and
                    p.project.is_ready == False):
                p.solve_project()

    def __str__(self):
        return "Mob_Departament"


@dataclass
class QA_Department(Department):

    def send_projects(self, project: Project):
        for p in self.programmers:
            if (p.is_busy == False and p.dismiss == False):
                p.accept_project(project)
                print(f'в отдел тестировки принят проект {p.project.id}')
                break

    def solve_projects(self):
        dir.get_QA_employees()
        for D in self.projects:
            if D.accepted_to_test == False:
                self.send_projects(D)

        for p in self.programmers:
            if (p.dismiss == False and
                    p.project.accepted_to_test == True and
                    p.project.is_ready_test == False):
                p.test_project()

        self.__delete_project()

    def __delete_project(self):
        # This function delete tested projects of all depatments
        i = 0
        while i < len(self.projects):
            if self.projects[i].is_ready_test:
                self.real_project += 1
                print(f'проект {self.projects[i]} реализован и удален из системы '
                      f'{self.projects[i].programmers}')
                s = self.projects[i]
                self.projects.remove(self.projects[i])
                try:
                    dir.departments[s.type_project].projects.remove(
                        self.projects[i])
                except Exception:
                    print(Exception.args)
                i -= 1
            i += 1

    def __str__(self):
        return "QA_Departament"

@dataclass
class Director:
    projects: list = field(default_factory=list)
    departments: dict = field(default_factory=dict)

    def get_employees(self):
        for project in self.projects:
            if ((project.type_project == 'web' or
                    project.type_project == 'mob') and
                    project.is_accepted == False):
                self.departments[project.type_project].add_programmers(project.type_project)

    def get_projects(self, day: int):
        self.projects = [Project(day) for _ in range(random.randint(0, 4))]

    def send_projects(self):
        self.departments['mob'].get_free_programmers()
        self.departments['web'].get_free_programmers()
        for project in self.projects:
            if ((project.type_project == 'web' or
                    project.type_project == 'mob') and
                    project.is_accepted == False):
                flag = self.departments[project.type_project].get_projects(project)
                if flag == True:
                    project.is_accepted = True
                else:
                    project.is_accepted = False

    def get_QA_employees(self):
        temp = dir.departments['web'].projects + dir.departments['mob'].projects
        self.departments['qa'].get_free_programmers()
        for project in temp:
            if project.to_test == True and project.accepted_to_test == False:
                flag = self.departments['qa'].get_projects(project)
                if not flag:
                    self.departments['qa'].add_programmers('test')


def create_departments():
    dir = Director()
    departments = {
        'web': Web_Department(),
        'mob': Mob_Department(),
        'qa': QA_Department()
    }
    dir.departments.update(departments)
    return dir

if __name__ == '__main__':
    days = 10
    dir = create_departments()

    def job():
        for k,v in dir.departments.items():
                v.solve_projects()

    for i in range(1, days):
        day = i
        print("day -", day)
        dir.get_employees()
        dir.send_projects()
        job()
        dir.get_projects(day)
        dir.send_projects()
        for i in dir.departments.keys():
            if i != 'qa':
                dir.departments[i]._dismiss()

        for i in dir.departments.keys():
                for p in dir.departments[i].programmers:
                    print(p)

        print('_____конец дня_____ :')
        print(f"кличесвто реализованных проектов {dir.departments['qa'].real_project}")
        print(f"количесвто нанятых сотрудников {Department.employes}")
        print(f"уволенные {Department.dismissed}")









