# -*- coding: utf-8 -*-
from settings import root_logger
import sys
import traceback
from sqlalchemy import create_engine, Column, Integer, Text, Boolean, asc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import exists

dbase = None
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

engine = create_engine(f"sqlite:///{dbase}")
session = sessionmaker(bind=engine)()
base = declarative_base()
# conn = session.bind
conn = engine.connect()
# ----------------------------------------------------Tables --------------------------------
class Οροφος_1(base):
    __tablename__ = 'Οροφος_1'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="1")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, nullable=False)
    serial = Column(Text, unique=True, nullable=False)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)

    # def __repr__(self):
    #     return "<Οροφος_1(id='%s', κωδικός='%s', όροφος='%s', τύπος='%s', μοντέλο='%s', serial='%s', γραφείο='%s'" \
    #            "αρχικός='%s', ημερ_αρχι='%s', τελικός='%s', ημερο_τελικ='%s', σύνολο='%s', toner_original='%s'" \
    #            "toner_symbato='%s', drum='%s', χρέωση='%s', σχόλια='%s')>" \
    #            % (self.ID, self.κωδικός, self.όροφος, self.τύπος, self.μοντέλο, self.serial, self.γραφείο,
    #               self.αρχικός, self.ημερ_αρχι, self.τελικός, self.ημερο_τελικ, self.σύνολο, self.toner_original,
    #               self.toner_symbato, self.drum, self.χρέωση, self.σχόλια)
    #
    # def __str__(self):
    #     return f"{self.κωδικός} {self.όροφος} {self.τύπος} {self.μοντέλο} {self.serial} {self.γραφείο} {self.αρχικός}" \
    #            f"{self.ημερ_αρχι} {self.τελικός} {self.ημερο_τελικ} {self.σύνολο} {self.toner_original}  \
    #            {self.toner_symbato} {self.drum} {self.χρέωση} {self.χρέωση} {self.σχόλια}"


class Οροφος_2(base):
    __tablename__ = 'Οροφος_2'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="2")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Οροφος_4(base):
    __tablename__ = 'Οροφος_4'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="4")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Οροφος_5(base):
    __tablename__ = 'Οροφος_5'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="5")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Οροφος_6(base):
    __tablename__ = 'Οροφος_6'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="6")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Πασιάς(base):
    __tablename__ = 'Πασιάς'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΗΜΙΟΡΟΦΟΣ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default="ΠΑΣΙΑΣ ΠΑΝΤΕΛΗΣ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Κτηνιατρείο(base):
    __tablename__ = 'Κτηνιατρείο'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΚΤΗΝΙΑΤΡΕΙΟ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Πρωτοβάθμια(base):
    __tablename__ = 'Πρωτοβάθμια'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΠΡΩΤΟΒΑΘΜΙΑ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Δευτεροβάθμια(base):
    __tablename__ = 'Δευτεροβάθμια'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΔΕΥΤΕΡΟΒΑΘΜΙΑ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Κτέο(base):
    __tablename__ = 'Κτέο'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΙΣΟΓΕΙΟ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Αμύνταιο(base):
    __tablename__ = 'Αμύνταιο'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΙΣΟΓΕΙΟ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Κεδασυ(base):
    __tablename__ = 'Κεδασυ'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="ΙΣΟΓΕΙΟ")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=True)


class Εκτός(base):
    __tablename__ = 'Εκτός'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    κωδικός = Column(Text, default=" ")
    όροφος = Column(Text, default="Εκτός")
    τύπος = Column(Text, default=" ")
    μοντέλο = Column(Text, default=" ")
    serial = Column(Text, unique=True)
    γραφείο = Column(Text, default=" ")
    αρχικός = Column(Integer, default=0)
    ημερ_αρχι = Column(Text, default=" ")
    τελικός = Column(Integer, default=0)
    ημερο_τελικ = Column(Text, default=" ")
    σύνολο = Column(Integer, default=τελικός - αρχικός)
    toner_original = Column(Text, default=" ")
    toner_symbato = Column(Text, default=" ")
    drum = Column(Text, default=" ")
    χρέωση = Column(Text, default=" ")
    σχόλια = Column(Text, default=" ")
    ενεργό = Column(Boolean, default=False)


tables = [Οροφος_1, Οροφος_2, Οροφος_4, Οροφος_5, Οροφος_6, Πασιάς, Κτηνιατρείο, Πρωτοβάθμια, Δευτεροβάθμια, Κτέο,
          Αμύνταιο, Εκτός, Κεδασυ]


def fetch_clicked_table_data(table):
    try:
        data = session.query(table).all()
        session.close()
        return data
    except Exception as error:
        print(f"Error fetch_clicked_table_data() {error}")
        traceback.print_exc()
        session.close()
        return


def fetch_all_table_data():
    all_data = []
    try:
        for table in tables:
            data = session.query(table).all()
            all_data.append(data)
        session.close()
        return all_data
    except Exception as error:
        print(f"Error fetch_all_table_data() {error}")
        traceback.print_exc()
        session.close()
        return


def get_total_counter():
    total_counter = 0
    try:
        for table in tables:
            data = session.query(table).all()
            for row in data:
                total_counter += row.σύνολο
        session.close()
        return total_counter
    except Exception as error:
        total_counter = "Σφάλμα"
        print(f"Error get_total_counter() {error}")
        traceback.print_exc()
        session.close()
        return total_counter


def get_item_from_table(table, item_id):
    try:
        item = session.query(table).get(int(item_id))
        # session.close() # Αν κλίνει δεν αποθηκεύει τις αλλαγές μετά
    except Exception as error:
        item = "Σφάλμα"
        print(f"Error get_item_from_table() {error}")
        session.close()
    return item


def get_item_data_from_all_tables(item_id, item_serial):
    try:
        for table in tables:
            item = session.query(table).filter(table.ID == item_id, table.serial == item_serial).scalar()
            if item:
                return item, table
            else:
                continue

        # session.close() # Αν κλίνει δεν αποθηκεύει τις αλλαγές μετά
    except Exception as error:
        print(f"Error fetch_all_table_data() {error}")
        traceback.print_exc()
        session.close()
        return


def get_my_machines():
    my_machines = []
    try:
        for table in tables:
            data = session.query(table).all()
            for item in data:
                if "ΔΙΚΟ" in item.κωδικός:
                    my_machines.append(item)

        session.close()
        return my_machines
    except Exception as error:
        print(f"Error get_my_machines() {error}")
        traceback.print_exc()
        session.close()
        return


def search_in_table(table, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στή βάση είναι ολα κεφαλαία αρα θέλει κεφαλαία για να βρει
    try:
        items = session.query(table).filter((table.κωδικός.ilike(last_like)) |
                                            (table.όροφος.ilike(last_like)) |
                                            (table.τύπος.ilike(last_like)) |
                                            (table.μοντέλο.ilike(last_like)) |
                                            (table.serial.ilike(last_like)) |
                                            (table.γραφείο.ilike(last_like)) |
                                            (table.αρχικός.ilike(last_like)) |
                                            (table.ημερ_αρχι.ilike(last_like)) |
                                            (table.τελικός.ilike(last_like)) |
                                            (table.ημερο_τελικ.ilike(last_like)) |
                                            (table.σύνολο.ilike(last_like)) |
                                            (table.toner_original.ilike(last_like)) |
                                            (table.toner_symbato.ilike(last_like)) |
                                            (table.drum.ilike(last_like)) |
                                            (table.χρέωση.ilike(last_like)) |
                                            (table.σχόλια.ilike(last_like))).order_by(asc(table.ID))
        session.close()
        return items
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def search_code_in_table(table, code_to_search):
    last_like = f"%{code_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στή βάση είναι ολα κεφαλαία αρα θέλει κεφαλαία για να βρει
    try:
        item = session.query(table).filter(table.κωδικός.ilike(last_like)).all()
        session.close()
        return item
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def search_in_all_tables(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    all_data = []
    # στή βάση είναι ολα κεφαλαία αρα θέλει κεφαλαία για να βρει
    try:
        for table in tables:
            item = session.query(table).filter((table.όροφος.ilike(last_like)) |
                                               (table.τύπος.ilike(last_like)) |
                                               (table.μοντέλο.ilike(last_like)) |
                                               (table.serial.ilike(last_like)) |
                                               (table.γραφείο.ilike(last_like)) |
                                               (table.αρχικός.ilike(last_like)) |
                                               (table.ημερ_αρχι.ilike(last_like)) |
                                               (table.τελικός.ilike(last_like)) |
                                               (table.ημερο_τελικ.ilike(last_like)) |
                                               (table.σύνολο.ilike(last_like)) |
                                               (table.toner_original.ilike(last_like)) |
                                               (table.toner_symbato.ilike(last_like)) |
                                               (table.drum.ilike(last_like)) |
                                               (table.χρέωση.ilike(last_like)) |
                                               (table.σχόλια.ilike(last_like))).all()
            if item:  # να αποφύγουμε κενές λίστες
                all_data.append(item)
        session.close()
        return all_data  # all_data έχει τη μορφή [[κάτι, δεύτερο],[τρίτο,τέταρτο],[πέμπτο]]
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def search_in_my_machines(text_to_search):
    last_like = f"{text_to_search.upper()}"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    my_machines = get_my_machines()
    all_data = []
    try:
        for machine in my_machines:
            if last_like in machine.όροφος or last_like in machine.τύπος or last_like in machine.μοντέλο \
                    or last_like in machine.serial or last_like in machine.γραφείο \
                    or last_like in machine.τύπος or last_like in machine.μοντέλο \
                    or last_like in str(machine.αρχικός) or last_like in str(machine.ημερ_αρχι) \
                    or last_like in str(machine.τελικός) or last_like in str(machine.ημερο_τελικ) \
                    or last_like in str(machine.σύνολο) or last_like in machine.toner_original \
                    or last_like in machine.toner_symbato or last_like in machine.drum \
                    or last_like in machine.χρέωση or last_like in machine.σχόλια:
                all_data.append(machine)
        session.close()
        return all_data
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def search_code_in_my_machines(text_to_search):
    my_machines = get_my_machines()
    all_data = []
    try:
        for machine in my_machines:
            if text_to_search in machine.κωδικός:
                all_data.append(machine)
        session.close()
        return all_data
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def search_code_in_all_machines(text_to_search):
    last_like = f"{text_to_search.upper()}"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    all_machines = fetch_all_table_data()
    all_data = []
    # στή βάση είναι ολα κεφαλαία αρα θέλει κεφαλαία για να βρει
    try:
        for floor in all_machines:
            for machine in floor:
                if last_like in machine.κωδικός:
                    all_data.append(machine)
        session.close()
        return all_data  # all_data έχει τη μορφή [[κάτι, δεύτερο],[τρίτο,τέταρτο],[πέμπτο]]
    except Exception as error:
        print(f"Error search() {error}")
        traceback.print_exc()
        session.close()
        return


def get_offices_from_table(table):
    offices = []
    for item in session.query(table).all():
        if item.γραφείο not in offices:
            offices.append(item.γραφείο)
    offices.sort()
    return offices
