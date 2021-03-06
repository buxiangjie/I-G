# -*- coding: UTF-8 -*-
"""
@auth:卜祥杰
@date:2020-06-23 14:51:00
@describe: 即分期医疗18期
"""
import os
import json
import sys
import time
import allure
import pytest

from common.common_func import Common
from log.logger import Logger
from common.open_excel import excel_table_byname
from config.configer import Config
from common.get_sql_data import GetSqlData

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = Logger(logger="test_jfqyl_18_periods_tp").getlog()

@allure.feature("即分期医疗18期")
class TestJfqyl18Tp:
	file = Config().get_item('File', 'jfq_case_file')

	@allure.title("进件申请")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_100_apply(self, r, env):
		"""进件申请"""
		data = excel_table_byname(self.file, 'apply')
		print("接口名称:%s" % data[0]['casename'])
		Common.p2p_get_userinfo('jfqyl_18_periods', env)
		r.mset(
			{
				"jfqyl_18_periods_sourceUserId": Common.get_random('userid'),
				"jfqyl_18_periods_transactionId": Common.get_random('transactionId'),
				"jfqyl_18_periods_phone": Common.get_random('phone'),
				"jfqyl_18_periods_sourceProjectId": Common.get_random('sourceProjectId'),
			}
		)
		param = json.loads(data[0]['param'])
		param.update(
			{
				"sourceProjectId": r.get('jfqyl_18_periods_sourceProjectId'),
				"sourceUserId": r.get('jfqyl_18_periods_sourceUserId'),
				"transactionId": r.get('jfqyl_18_periods_transactionId')
			}
		)
		param['applyInfo'].update(
			{
				"applyTime": Common.get_time("-"),
				"applyAmount": 33333.33,
				"applyTerm": 18,
				"productCode": "FQ_JK_JFQYL"
			}
		)
		param['loanInfo'].update(
			{
				"loanAmount": 33333.33,
				"loanTerm": 18,
				"assetInterestRate": 0.153,
				"userInterestRate": 0.153
			}
		)
		param['personalInfo'].update(
			{
				"cardNum": r.get('jfqyl_18_periods_cardNum'),
				"custName": r.get('jfqyl_18_periods_custName'),
				"phone": r.get('jfqyl_18_periods_phone')
			}
		)
		param['applyInfo'].update({"applyTime": Common.get_time("-")})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		r.set('jfqyl_18_periods_projectId', rep['content']['projectId'])
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("上传授信协议")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_101_sign_credit(self, r, env):
		"""上传授信协议"""
		data = excel_table_byname(self.file, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = Common.get_json_data('data', 'jfq_sign_credit.json')
		param.update(
			{
				"serviceSn": Common.get_random('serviceSn'),
				"sourceUserId": r.get('jfqyl_18_periods_sourceUserId'),
				"contractType": 5,
				"sourceContractId": Common.get_random('userid'),
				"transactionId": r.get('jfqyl_18_periods_transactionId'),
				"associationId": r.get('jfqyl_18_periods_projectId')
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("进件结果查询")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_102_query_apply_result(self, r, env):
		"""进件结果查询"""
		GetSqlData.change_project_audit_status(
			project_id=r.get('jfqyl_18_periods_projectId'),
			environment=env
		)
		data = excel_table_byname(self.file, 'query_apply_result')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"sourceProjectId": r.get('jfqyl_18_periods_sourceProjectId'),
				"projectId": r.get('jfqyl_18_periods_projectId')
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])
		assert rep['content']['auditStatus'] == 2

	@allure.title("上传借款协议")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_103_sign_borrow(self, r, env):
		"""上传借款协议"""
		data = excel_table_byname(self.file, 'contract_sign')
		print("接口名称:%s" % data[0]['casename'])
		param = Common.get_json_data('data', 'jfq_sign_borrow.json')
		param.update(
			{
				"serviceSn": Common.get_random('serviceSn'),
				"sourceUserId": r.get('jfqyl_18_periods_sourceUserId'),
				"sourceContractId": Common.get_random('userid'),
				"transactionId": r.get('jfqyl_18_periods_transactionId'),
				"associationId": r.get('jfqyl_18_periods_projectId')
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		r.set("jfqyl_18_periods_contractId", rep['content']['contractId'])
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("上传图片")
	@allure.severity("normal")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_105_image_upload(self, r, env):
		"""上传图片"""
		data = excel_table_byname(self.file, 'image_upload')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"associationId": r.get('jfqyl_18_periods_projectId')})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("签章结果查询")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_106_contact_query(self, r, env):
		"""合同结果查询:获取签章后的借款协议"""
		data = excel_table_byname(self.file, 'contract_query')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"associationId": r.get('jfqyl_18_periods_projectId'),
				"serviceSn": Common.get_random("serviceSn"),
				"requestTime": Common.get_time("-"),
				"sourceUserId": r.get("jfqyl_18_periods_sourceUserId"),
				"contractId": r.get("jfqyl_18_periods_contractId")
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("还款计划试算")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_107_calculate(self, r, env):
		"""还款计划试算（未放款）:正常还款"""
		data = excel_table_byname(self.file, 'calculate')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"sourceUserId": r.get("jfqyl_18_periods_sourceUserId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"projectId": r.get("jfqyl_18_periods_projectId")
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("放款申请")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_108_loan_pfa(self, r, env):
		"""放款申请"""
		data = excel_table_byname(self.file, 'loan_pfa')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		r.set("jfqyl_18_periods_loan_serviceSn", Common.get_random("serviceSn"))
		param.update(
			{
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"sourceUserId": r.get("jfqyl_18_periods_sourceUserId"),
				"serviceSn": r.get("jfqyl_18_periods_loan_serviceSn"),
				"id": r.get('jfqyl_18_periods_cardNum'),
				"accountName": r.get("jfqyl_18_periods_custName"),
				"amount": 33333.33
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])
		# 修改支付表中的品钛返回code
		time.sleep(8)
		GetSqlData.change_pay_status(
			environment=env,
			project_id=r.get('jfqyl_18_periods_projectId')
		)

	@allure.title("放款结果查询")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_109_loan_query(self, r, env):
		"""放款结果查询"""
		GetSqlData.loan_set(environment=env, project_id=r.get('jfqyl_18_periods_projectId'))
		data = excel_table_byname(self.file, 'pfa_query')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update({"serviceSn": r.get("jfqyl_18_periods_loan_serviceSn")})
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])
		assert rep['content']['projectLoanStatus'] == 3

	@allure.title("还款计划查询")
	@allure.severity("blocker")
	@pytest.mark.asset
	@pytest.mark.offline_repay
	@pytest.mark.offline_settle_in_advance
	@pytest.mark.returns
	def test_110_query_repayment_plan(self, r, env):
		"""国投云贷还款计划查询"""
		data = excel_table_byname(self.file, 'query_repayment_plan')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"projectId": r.get("jfqyl_18_periods_projectId")
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		r.set("jfqyl_18_periods_repayment_plan", json.dumps(rep['content']['repaymentPlanList']))
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("提前结清试算")
	@allure.severity("blocker")
	@pytest.mark.offline_settle_in_advance
	def test_111_calculate(self, r, env):
		"""还款计划试算:提前结清"""
		data = excel_table_byname(self.file, 'calculate')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"sourceUserId": r.get("jfqyl_18_periods_sourceUserId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"businessType": 2
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		r.set(
			"jfqyl_18_periods_early_settlement_repayment_plan",
			json.dumps(rep['content']['repaymentPlanList'])
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("退货试算")
	@allure.severity("blocker")
	@pytest.mark.returns
	def test_112_calculate(self, r, env):
		"""还款计划试算:退货"""
		data = excel_table_byname(self.file, 'calculate')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		param.update(
			{
				"sourceUserId": r.get("jfqyl_18_periods_sourceUserId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"businessType": 3
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		r.set(
			"jfqyl_18_periods_return_repayment_plan",
			json.dumps(rep['content']['repaymentPlanList'])
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("还款流水推送")
	@allure.severity("blocker")
	@pytest.mark.offline_repay
	def test_113_offline_repay_repayment(self, r, env):
		"""线下还款流水推送：正常还一期"""
		data = excel_table_byname(self.file, 'offline_repay')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		period = 1
		plan_pay_date = GetSqlData.get_repayment_detail(
			project_id=r.get("jfqyl_18_periods_projectId"),
			environment=env,
			period=period,
			repayment_plan_type=1
		)
		repayment_plan_list = r.get("jfqyl_18_periods_repayment_plan")
		success_amount = 0.00
		repayment_detail_list = []
		for i in json.loads(repayment_plan_list):
			if i['period'] == period:
				plan_detail = {
					"sourceRepaymentDetailId": Common.get_random("transactionId"),
					"payAmount": i['restAmount'],
					"planCategory": i['repaymentPlanType']
				}
				success_amount = round(success_amount + float(plan_detail.get("payAmount")), 2)
				repayment_detail_list.append(plan_detail)
		param.update(
			{
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceRepaymentId": Common.get_random("sourceProjectId"),
				"planPayDate": str(plan_pay_date['plan_pay_date']),
				"successAmount": success_amount,
				"payTime": Common.get_time("-"),
				"period": period
			}
		)
		param['repaymentDetailList'] = repayment_detail_list
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("提前全部结清")
	@allure.severity("blocker")
	@pytest.mark.offline_settle_in_advance
	def test_114_offline_nrepay_early_settlement(self, r, env):
		"""线下还款流水推送：提前全部结清"""
		data = excel_table_byname(self.file, 'offline_repay')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		plan_pay_date = GetSqlData.get_repayment_detail(
			project_id=r.get("jfqyl_18_periods_projectId"),
			environment=env,
			period=1,
			repayment_plan_type=1
		)
		repayment_plan_list = json.loads(r.get("jfqyl_18_periods_early_settlement_repayment_plan"))
		success_amount = 0.00
		repayment_detail_list = []
		for i in repayment_plan_list:
			plan_detail = {
				"sourceRepaymentDetailId": Common.get_random("transactionId"),
				"payAmount": i['amount'],
				"planCategory": i['repaymentPlanType']
			}
			success_amount = round(success_amount + plan_detail.get("payAmount"), 2)
			repayment_detail_list.append(plan_detail)
		param.update(
			{
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceRepaymentId": Common.get_random("sourceProjectId"),
				"planPayDate": str(plan_pay_date['plan_pay_date']),
				"successAmount": success_amount,
				"repayType": 2,
				"period": repayment_plan_list[0]['period'],
				"payTime": Common.get_time("-")
			}
		)
		param['repaymentDetailList'] = repayment_detail_list
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("退货")
	@allure.severity("blocker")
	@pytest.mark.returns
	def test_116_return(self, r, env):
		"""退货"""
		data = excel_table_byname(self.file, 'offline_repay')
		print("接口名称:%s" % data[0]['casename'])
		param = json.loads(data[0]['param'])
		plan_pay_date = GetSqlData.get_repayment_detail(
			project_id=r.get("jfqyl_18_periods_projectId"),
			environment=env,
			period=1,
			repayment_plan_type=1
		)
		repayment_plan_list = json.loads(r.get("jfqyl_18_periods_return_repayment_plan"))
		success_amount = 0.00
		repayment_detail_list = []
		for i in repayment_plan_list:
			plan_detail = {
				"sourceRepaymentDetailId": Common.get_random("transactionId"),
				"payAmount": i['amount'],
				"planCategory": i['repaymentPlanType']
			}
			success_amount = round(success_amount + plan_detail.get("payAmount"), 2)
			repayment_detail_list.append(plan_detail)
		param.update(
			{
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"transactionId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"sourceRepaymentId": Common.get_random("sourceProjectId"),
				"planPayDate": str(plan_pay_date['plan_pay_date']),
				"successAmount": success_amount,
				"repayType": 3,
				"period": repayment_plan_list[0]['period'],
				"payTime": Common.get_time("-")
			}
		)
		param['repaymentDetailList'] = repayment_detail_list
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			product="cloudloan",
			environment=env
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])

	@allure.title("资金流水推送")
	@allure.severity("blocker")
	@pytest.mark.offline_repay
	def test_117_capital_flow(self, r, env):
		"""资金流水推送"""
		data = excel_table_byname(self.file, 'cash_push')
		param = json.loads(data[0]['param'])
		success_amount = GetSqlData.get_repayment_amount(
			project_id=r.get("jfqyl_18_periods_projectId"),
			environment=env,
			period=1
		)
		param.update(
			{
				"serviceSn": Common.get_random("serviceSn"),
				"productCode": "FQ_JK_JFQYL",
				"projectId": r.get("jfqyl_18_periods_projectId"),
				"sourceProjectId": r.get("jfqyl_18_periods_sourceProjectId"),
				"repaymentPlanId": Common.get_random("sourceProjectId"),
				"sucessAmount": success_amount,
				"sourceRepaymentId": Common.get_random("sourceProjectId"),
				"tradeTime": Common.get_time(),
				"finishTime": Common.get_time()
			}
		)
		if len(data[0]['headers']) == 0:
			headers = None
		else:
			headers = json.loads(data[0]['headers'])
		rep = Common.response(
			faceaddr=data[0]['url'],
			headers=headers,
			data=json.dumps(param, ensure_ascii=False),
			environment=env,
			product="cloudloan"
		)
		assert rep['resultCode'] == int(data[0]['resultCode'])


if __name__ == '__main__':
	pytest.main()
