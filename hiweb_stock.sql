select s1.branchno,
	s1.stockno,
	s1.stockdate,
	s1.customercode,
	s1.salecode,
	(case
		when s2.model like '1T%' then 'Pick up'
		when s2.model like 'MU-X' then 'MU-X'
		when s2.submodel like any (array['NPR%','NQR%']) then '3T Small'
		when s2.submodel like any (array['FRR%']) then '3T Big'
		when s2.submodel like any (array['FVM%']) then '10W(6X2)'
		when s2.submodel like any (array['FVZ%', 'FXZ%']) then '10W(6X4)'
		else s2.model
	end) as car_category_sales,
	(case 
		when s2.submodel like 'NLR77%' then 'NLR Lite'
		when s2.submodel like 'NMR85__FXU%' then 'NMR Mixer'
		when s2.submodel like 'FRR90HNXF%' then 'FRR Short 190 เฟืองเร็ว'
		when s2.submodel like 'FRR90HSXF%' then 'FRR Short 210 เฟืองเร็ว'
		when s2.submodel like 'FRR90HSXT%' then 'FRR Short 210 max torque'
		when s2.submodel like 'FRR90HNF%' then 'FRR Mixer'
		when s2.submodel like 'FRR90LN%' then 'FRR Medium 190' 
		when s2.submodel like 'FRR90LS%' then 'FRR Medium 210'
		when s2.submodel like 'FRR90NN%' then 'FRR Long 190'
		when s2.submodel like 'FRR90NS%' then 'FRR Long 210'
		when s2.submodel like 'FXZ60__FXU%' then 'FXZ Mixer'
		when s2.model like any (array['1T%','MU-X']) then s2.model
		else left(s2.submodel, 3)
	end) as model_sales,
	right(s2.enginno, 6) as enginno
from tblmststock s1
left join tbldtlstock s2
using (stockno)
where s1.stockno != ''
	and s1.branchno != '00'
	and s1.stockno not similar to '[^0-9][^0-9]%'
	and s2.model like any(array['2-T%', '3-T%', '6-T%', '10-W%', '12-W%', 'T/H%'])