<?php
/**
 * Version endpoint for the AI Server API.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api\Endpoints;

use SS_AI_Image_Search\Api\Client;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Version endpoint class for version information.
 */
class VersionEndpoint {

	/**
	 * API Client instance.
	 *
	 * @var Client
	 */
	private Client $client;

	/**
	 * Constructor.
	 *
	 * @param Client $client API Client instance.
	 */
	public function __construct( Client $client ) {
		$this->client = $client;
	}

	/**
	 * Get API version information.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_version(): Response {
		$endpoint = 'version';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get server version information.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_server_version(): Response {
		$endpoint = 'version/server';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get plugin version information.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_plugin_version(): Response {
		$endpoint = 'version/plugin';

		return $this->client->get( $endpoint );
	}

	/**
	 * Get API compatibility information.
	 *
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function get_compatibility(): Response {
		$endpoint = 'version/compatibility';

		return $this->client->get( $endpoint );
	}

	/**
	 * Check if version is compatible.
	 *
	 * @param string $version Version to check.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	public function check_compatibility( string $version ): Response {
		$endpoint = 'version/compatibility/check';

		$query_params = array(
			'version' => $version,
		);

		return $this->client->get( $endpoint, $query_params );
	}
}