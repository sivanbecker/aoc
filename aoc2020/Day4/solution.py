from marshmallow import Schema, fields, validate, ValidationError
import re


def validate_pid(pid):
    """ Passport ID - a nine-digit number, including leading zeroes."""
    if not re.match("^[0-9]{9}$", pid):
        raise ValidationError(f"Wrong Passport ID format {pid}")


def validate_hcl(hcl):
    """ Hair Color - a # followed by exactly six characters 0-9 or a-f."""
    if not re.match("^#[0-9a-f]{6}$", hcl):
        raise ValidationError(f"Wrong Hair Color format {hcl}")


def validate_hgt(hgt):
    """Height) - a number followed by either cm or in:

    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76."""
    cm = re.match(r"^(\d{3})cm$", hgt)
    inch = re.match(r"(\d{2})in", hgt)
    if cm and (int(cm.groups()[0]) < 150 or int(cm.groups()[0]) > 193):
        raise ValidationError(f"Heigth in cm is out of range for {cm.groups()[0]}")
    if inch and (int(inch.groups()[0]) < 59 or int(inch.groups()[0]) > 76):
        raise ValidationError(f"Heigth in inchs is out of range for {inch.groups()[0]}")

    if not cm and not inch:
        raise ValidationError(f"Not cm and not Inch value")


class PassportSchema(Schema):
    byr = fields.Int(required=True, validate=validate.Range(min=1920, max=2002))
    iyr = fields.Int(required=True, validate=validate.Range(min=2010, max=2020))
    eyr = fields.Int(required=True, validate=validate.Range(min=2020, max=2030))
    hgt = fields.Str(required=True, validate=validate_hgt)
    hcl = fields.Str(required=True, validate=validate_hcl)
    ecl = fields.Str(
        required=True,
        validate=validate.OneOf(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]),
    )
    pid = fields.Str(required=True, validate=validate_pid)
    cid = fields.Str(required=False)


schema = PassportSchema()


class Day4:

    _MUST_FIELDS = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }

    def __init__(self, input_file, part1=True):
        self.valid = 0
        self._load_passports_part1(input_file) if part1 else self._load_passports_part2(
            input_file
        )

    def _load_passports_part2(self, infile):
        lines = self._file_lines(infile)
        passports = self._passport_seperator(lines)
        counter = 0
        for p in passports:
            try:
                rec = schema.load(p)
                self.valid += 1
            except ValidationError as e:
                pass

    def _load_passports_part1(self, infile):
        lines = self._file_lines(infile)
        passports = self._passport_seperator(lines)
        counter = 0
        for p in passports:
            if all(k in p for k in self._MUST_FIELDS):
                self.valid += 1

    def _file_lines(self, infile):
        with open(infile, "r") as fh:
            for line in fh:

                yield line.strip()

    def _passport_seperator(self, lines):
        p = []
        for line in lines:
            if line:
                p.extend(line.split())
            else:
                yield {k: v for k, v in (pattr.split(":") for pattr in p)}
                p = []
                next
        yield {k: v for k, v in (pattr.split(":") for pattr in p)}

    def valid_recs(self):
        return self.valid


def test_dummy():

    assert Day4("dummy.txt").valid_recs() == 2


def test_invalid():
    assert Day4("invalid_input.txt", part1=False).valid_recs() == 0


def test_valid():
    assert Day4("valid_input.txt", part1=False).valid_recs() == 4


def test_input():
    assert Day4("input.txt").valid_recs() == 237
    assert Day4("input.txt", part1=False).valid_recs() == 172


if __name__ == "__main__":
    sl = Day4("input.txt")
    print(sl.valid)