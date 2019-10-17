#        float rhigh;        // 高值
#        float rlow;         // 低值
#        float high;         //包含处理后的高值
#        float low;          //包含处理后的低值
#        int    flag;        //1顶 -1底 0 非顶底
#        float fxqj;         // 分型区间 如果为顶底 记录区间边界
#        int dir;            //K线方向 1上 -1下 2 上包含 -2 下包含
#        int bi;             //笔 1上 -1下 2 上包含 -2 下包含
#        int duan;           //段 1上 -1下 2 上包含 -2 下包含
#        int noh;            // 高点K线编号
#        int nol;            // 低点K线编号
#        float high;         // 高点
#        float low;          // 低点
#        int dir;            // 方向 方向 1上 -1下 2 上包含 -2 下包含
#        int flag;           // 1顶 -1底
#        int qk;             // 特征1 2 之间是否存在缺口
#        int binum;          // 包含几笔
#        int duanno;         // 段序号
#        int flag;           // 走势方向 1上 -1下
#        int ksno;           // zg所在K线NO (有zg必有zd)
#        int jsno;           // zd所在K线NO
#        int znnum;          // 包含zn数
#        float zg;           // ZG=min(g1、g2)
#        float zd;           // ZD=max(d1、d2)
#        float gg;           // GG=max(gn);
#        float dd;           // dd=min(dn);
#        float zz;           // 震荡中轴(监视器)
# QK 缺口
# dir = DIR_SBH #上包含
# dir = DIR_XBH #下包含
# jg2 = 0间隔  # 至少5根K线