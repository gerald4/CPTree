import ANDORsearch.ANDORSearch
import DataManipulation.{Data, FileFormat}
import DecisionTree.DTree
import oscar.cp.core.CPStore

object RunTreeANDOR {

  def run(file: String,
          format: FileFormat,
          TO: Int,
          isComplete: Boolean,
          depth: Int,
          lbLeaf: Int,
          lbLeafPercent: Boolean,
          heuristic: Int,
          isPrunningMinActive: Boolean = true,
          isCacheActive: Boolean = true
         ): String = {

    val t = System.currentTimeMillis()
    implicit val solver = new CPStore()

    val db = Data(file, format)

    val tree = DTree(depth, solver, db)
    tree.countP.assign(db.nbTransP)
    tree.countM.assign(db.nbTransM)



    if (isComplete)
      tree.cstRemoveDecision(0)

    var threshold = lbLeaf
    if (lbLeafPercent)
      threshold = db.nbTrans * threshold / 100

    tree.cstCountSum
    tree.cstSumMini
    tree.cstLeftMostCountSum
    if (threshold > 0) {
      tree.cstLeafThreshold(threshold)
      tree.cstSplitPossible(threshold)
    }
    tree.cstDummy
    tree.cstCoverSize
    tree.cstAllDiffExcept0Path
    tree.cstSplitUseful
    tree.cstRemoveUseless(threshold)
    heuristic match {
      case 0 => tree.computeValueOrderingLexico
      case 1 => tree.computeValueOrderingEntropy
      case 2 => tree.computeValueOrdering
    }


    val t1 = System.currentTimeMillis()
    val (sol_tree, cost_tree) = if (isPrunningMinActive && isCacheActive) {
      ANDORSearch.search(solver, tree, TO)
    } else if (isCacheActive) {
      ANDORSearch.searchNoMin(solver, tree, TO)
    } else {
      ANDORSearch.searchNoCache(solver, tree, TO)
    }
    val t2 = System.currentTimeMillis()
    println("Total time: " + (t2 - t) )

    if(cost_tree < Int.MaxValue)
      sol_tree
    else
      "NOSOL"

  }


}