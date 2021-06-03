from oslo_log import log

from ceilometer.network.services import base
from ceilometer import sample

LOG = log.getLogger(__name__)


class RouterPollster(base.BaseServicesPollster):

    FIELDS = [
        "status",
    ]

    @property
    def default_discovery(self):
        return "router_services"

    def get_samples(self, manager, cache, resources):

        for router in resources or []:
            LOG.debug("router: %s", router)
            if router["status"] is None:
                LOG.warning("Invalid status, skipping router %s" % router)
                continue
            status = self.get_status_id(router["status"])
            yield sample.Sample(
                name="router",
                type=sample.TYPE_GAUGE,
                unit="router",
                volume=status,
                user_id=router.get("user_id"),
                project_id=router["tenant_id"],
                resource_id=router["id"],
                resource_metadata=self.extract_metadata(router),
            )
