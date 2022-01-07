import unittest, re
from string import ascii_letters
from simple_atm_controller.exceptions import InvalidAccount, InvalidValidationRule
from simple_atm_controller.account import Account, AccountValidationRule
from simple_atm_controller.pin import Pin


class AccountIdTestCase(unittest.TestCase):
    # 필요한 데이터 만들기
    def setUp(self) -> None:
        self.pin_number = Pin("0000-0001")
    # pin_num넣었을 때 해당 계정나오는지 test(s) 
    def test_allocate_account_id(self):
        account_id = Account(self.pin_number, "IML")
        self.assertEqual(account_id.pin_number, "0000-0001")
        self.assertEqual(account_id.account_id, "IML")
        self.assertEqual(account_id.items, ("0000-0001", "IML"))
    
    # 핀번호 넣었는데 유효하지 않은 계정들 나올 때 test(f)
    def test_default_exception(self):
        invalid_account_ids = [ # 유효하지 않은 계정id들
            1, .1, ["0000"], ("0000",),
            {"0000"}, {"0000":"0000"},
            # ..., Anything that isn't a string
        ]
        for account_i in invalid_account_ids:
            try:
                Account(self.pin_number, account_i)
                self.assertTrue(False)
            except InvalidAccount:
                pass

    def test_custom_validation_rule(self):
        # custom된 계정 valiidation 유효한 값 나오나 확인(f)
        class CustomAccountRule(AccountValidationRule):
            def validate(self, pin_number) -> bool:
                # example valid format: 0000, 0001, ...
                return bool(re.search(r"\d{4}", pin_number))
     
        valid_id_list = ['{0:04d}'.format(i) for i in range(10000)]
        for valid_id_i in valid_id_list: 
            Account(self.pin_number, valid_id_i, CustomAccountRule())
            
        for idx in range(len(ascii_letters)): 
            try: 
                Account(
                    self.pin_number,
                    ascii_letters[idx: idx + 4],
                    CustomAccountRule()
                )
                self.assertTrue(False)
            except InvalidAccount:
                pass

    def test_invalid_validation_rule_exception(self):
        # 계정 유효한지 rule 상속받아서 확인
        class GoodRule(AccountValidationRule):
            def validate(self, account_id) -> bool:
                return True
        # 유효하지 않은 계정 확인하는 것 test
        class InvalidReturnRule(AccountValidationRule):
            def validate(self, account_id) -> bool:
                return "True" 

        class NotRule: 
            pass

        testcase = [ # testcase에 세개 클래스 넣어주고 test 돌려준다
            (GoodRule(), True),
            (InvalidReturnRule(), False),
            (NotRule(), False),
        ]

        for rule, expect in testcase:
            try:
                Account(self.pin_number, "something", rule) 
                self.assertTrue(expect) 
            except InvalidValidationRule: 
                self.assertFalse(expect)


if __name__ == '__main__':
    unittest.main()