from cudatext import *

FOLD_HINT = 'From selection'

class Command:
    def fold_sel(self):
        carets = ed.get_carets()
        if len(carets)>1:
            msg_status('Need single selection')
            return

        x1, y1, x2, y2 = carets[0]
        if x2<0:
            msg_status('Need single selection')
            return

        #sort coords
        if (y1,x1)>(y2,x2):
            x1, y1, x2, y2 = x2, y2, x1, y1

        if x2==0:
            y2 -= 1

        if y1==y2:
            msg_status('Cannot fold one-line selection')
            return

        ed.set_caret(0, y1)
        self.fold_rng(y1, y2, True)
        ed.set_prop(PROP_TAG, 'foldsel:%d,%d'%(y1,y2))
        msg_status('Folded selection')

    def fold_rng(self, y1, y2, and_fold):

        ed.folding(FOLDING_ADD, index=-1, item_x=0, item_y=y1, item_y2=y2, item_hint=FOLD_HINT)
        if and_fold:
            l = ed.folding(FOLDING_GET_LIST)
            if not l:
                return
            ed.folding(FOLDING_FOLD, index=len(l)-1)


    def on_change_slow(self, ed_self):

        s = ed.get_prop(PROP_TAG, 'foldsel:')
        if not s: return
        y1, y2 = map(int, s.split(','))
        self.fold_rng(y1, y2, True) #False not nice
