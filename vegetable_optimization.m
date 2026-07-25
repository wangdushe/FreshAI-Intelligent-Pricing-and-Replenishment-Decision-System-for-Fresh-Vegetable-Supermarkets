clc;
clear;


%% ==========================
% 生鲜蔬菜定价补货优化模型
% MATLAB
%% ==========================


% 成本

cost=3.5;


% 预测销量

demand=130;


% 损耗率

loss=0.1;



%% ==========================
% 优化变量
%
% x(1)=售价
%
% x(2)=补货量
%% ==========================



% 初始值

x0=[
5;
130
];



%% ==========================
% 利润函数
%% ==========================


profit=@(x) ...


-(

(x(1)-cost)*min(x(2),demand)

-cost*x(2)*loss

);



%% ==========================
% 约束
%% ==========================


% 售价范围

lb=[
cost;
50
];


ub=[
10;
300
];



%% ==========================
% 求解
%% ==========================


options=optimoptions(
'fmincon',
'Display',
'iter'
);



[x,fval]=fmincon(

profit,...
x0,...
[],[],
[],[],
lb,...
ub,...
[],...
options

);



%% ==========================
% 输出结果
%% ==========================



price=x(1);

stock=x(2);


profit_value=-fval;



fprintf(
'最优售价 %.2f 元/kg\n',
price
);


fprintf(
'最优补货量 %.2f kg\n',
stock
);


fprintf(
'最大利润 %.2f 元\n',
profit_value
);



%% ==========================
% 绘图
%% ==========================


figure


bar(
[
price,
stock,
profit_value
]
)


set(gca,...
'XTickLabel',...
{
'Price'
'Stock'
'Profit'
}
)


title(
'Optimization Result'
)
